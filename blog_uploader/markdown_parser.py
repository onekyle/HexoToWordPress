import markdown
import frontmatter
import datetime
from blog_uploader.logger import setup_logger

logger = setup_logger()

def parse_markdown(path):
    try:
        logger.info(f"开始解析Markdown文件: {path}")
        post = frontmatter.load(path)
        post_title = post.metadata.get('title', None)
        post_tags = post.metadata.get('tags', None)
        post_category = post.metadata.get('category', None)
        post_categories = post.metadata.get('categories', None)
        date = post.metadata.get('date', datetime.datetime.today())
        post_date = date
        post_content = convert_md2html(post.content)
        index_img = post.metadata.get('index_img', None)
        
        logger.info(f"成功解析文件: {path}")
        logger.debug(f"标题: {post_title}")
        logger.debug(f"标签: {post_tags}")
        logger.debug(f"分类: {post_categories}")
        logger.debug(f"特色图片: {index_img}")
        
        return post_title, post_tags, post_category, post_categories, post_date, post_content, index_img
    except Exception as e:
        logger.error(f"解析Markdown文件失败: {path}, 错误: {str(e)}")
        raise

def convert_md2html(content):
    try:
        return markdown.markdown(content, output_format='html5', extensions=['extra'])
    except Exception as e:
        logger.error(f"转换Markdown到HTML失败: {str(e)}")
        raise