import os
import requests
import tempfile
from urllib.parse import urlparse
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media
from blog_uploader.config import WORDPRESS_XMLRCPATH, WORDPRESS_USER_NAME, WORDPRESS_USER_PASSWD
from blog_uploader.logger import setup_logger

logger = setup_logger()

wp = Client(WORDPRESS_XMLRCPATH, WORDPRESS_USER_NAME, WORDPRESS_USER_PASSWD)

def download_image(url):
    try:
        logger.info(f"开始下载图片: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # 从URL中获取文件名
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = 'downloaded_image.jpg'
            
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
        
        # 下载图片到临时文件
        with open(temp_file.name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        logger.info(f"图片下载成功: {url} -> {temp_file.name}")
        return temp_file.name
    except Exception as e:
        logger.error(f"下载图片失败: {url}, 错误: {str(e)}")
        return None

def publish_post(post_title, post_tags, post_category, post_categories, post_date, post_content, thumbnail):
    try:
        logger.info(f"开始发布文章: {post_title}")
        post = WordPressPost()
        post.title = post_title
        post.date = post_date
        post.thumbnail = upload_image_if_needed(thumbnail)
        post.content = post_content
        
        # 处理分类
        categories = []
        if post_categories:
            if isinstance(post_categories, list):
                categories.extend(post_categories)
            else:
                categories.append(post_categories)
        if post_category:
            categories.append(post_category)
        
        terms_names = {
            'post_tag': post_tags,
            'category': categories,
        }
        post.terms_names = terms_names
        post.post_status = 'publish'
        
        logger.debug(f"文章信息: 标题={post_title}, 标签={post_tags}, 分类={categories}")
        wp.call(NewPost(post))
        logger.info(f"文章发布成功: {post_title}")
    except Exception as e:
        logger.error(f"发布文章失败: {post_title}, 错误: {str(e)}")
        raise

def upload_image_if_needed(image_name):
    if image_name is None:
        return None
        
    # 检查是否是URL
    if image_name.startswith(('http://', 'https://')):
        logger.info(f"检测到网络图片: {image_name}")
        image_name = download_image(image_name)
        if not image_name:
            return None
            
    if not os.path.exists(image_name):
        logger.warning(f"图片文件不存在: {image_name}")
        return None
        
    # 获取文件扩展名
    ext = os.path.splitext(image_name)[1].lower()
    # 根据扩展名设置MIME类型
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    mime_type = mime_types.get(ext, 'image/jpeg')
    
    try:
        logger.info(f"开始上传图片: {image_name}")
        with open(image_name, 'rb') as img:
            imageData = {
                'name': os.path.basename(image_name),
                'type': mime_type,
                'bits': xmlrpc_client.Binary(img.read()),
            }
        response = wp.call(media.UploadFile(imageData))
        image_id = response.get('id', None)
        logger.info(f"图片上传成功: {image_name}, ID: {image_id}")
        
        # 如果是临时文件，删除它
        if image_name.startswith(tempfile.gettempdir()):
            os.unlink(image_name)
            logger.debug(f"删除临时文件: {image_name}")
            
        return image_id
    except Exception as e:
        logger.error(f"上传图片失败: {image_name}, 错误: {str(e)}")
        if image_name.startswith(tempfile.gettempdir()):
            os.unlink(image_name)
            logger.debug(f"删除临时文件: {image_name}")
        return None