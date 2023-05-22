from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media
from blog_uploader.config import WORDPRESS_XMLRCPATH, WORDPRESS_USER_NAME, WORDPRESS_USER_PASSWD

wp = Client(WORDPRESS_XMLRCPATH, WORDPRESS_USER_NAME, WORDPRESS_USER_PASSWD)

def publish_post(post_title, post_tags, post_category, post_date, post_content, thumbnail):
    post = WordPressPost()
    post.title = post_title
    post.date = post_date
    post.thumbnail = upload_image_if_needed(thumbnail)
    post.content = post_content
    terms_names = {
        'post_tag': post_tags,
        'category': post_category,
    }
    post.terms_names = terms_names
    post.post_status = 'publish'
    wp.call(NewPost(post))

def upload_image_if_needed(image_name):
    if image_name is None:
        return None
    with open(image_name, 'rb') as img:
        imageData = {
            'name': image_name,
            'type': 'image/jpeg',
            'bits': xmlrpc_client.Binary(img.read()),
        }
    response = wp.call(media.UploadFile(imageData))
    return response.get('id', None)