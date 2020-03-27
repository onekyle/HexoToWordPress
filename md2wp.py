# coding=utf-8
'''
@Author: Kyle
@Date: 2020-03-05 08:34:04
@LastEditors: Kyle
@LastEditTime: 2020-03-28 01:33:34
@Description: 
@FilePath: /MarkdownToWordPress/md2wp.py
'''

import sys
import markdown
import frontmatter
import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import os
import re
from urllib.request import urlretrieve
import threading
import resize_image


def run(path: str, imgname: str, wp: Client):
    print('start: %s' % path)
    post = frontmatter.load(path)
    # 将获取到的信息赋值给变量
    # print(post.metadata)
    post_title = post.metadata.get('title', None)
    post_tags = post.metadata.get('tags', None)
    post_category = post.metadata.get('category', None)
    date = post.metadata.get('date', datetime.date.today())
    post_date = date
    post_content = post.content

    # convert
    post_content_html = convertMd2HTML(post_content)
    # publish
    # 现在就很简单了，通过下面的函数，将刚才获取到数据赋给对应的位置
    post = WordPressPost()
    post.title = post_title
    post.date = post_date
    # print(post_title)
    # post.slug文章别名
    # 我网站使用%postname%这种固定链接不想一长串，这里是最初md文章URL的参数，英文连字符格式
    # post.slug = post_url

    post.thumbnail = uploadImageIfNeed(imgname, wp=wp)
    # print("上传图片成功. id=" + post.thumbnail)
    post.content = post_content_html
    # 分类和标签
    terms_names = {}
    terms_names['post_tag'] = post_tags
    terms_names['category'] = post_category
    post.terms_names = terms_names
    # post.post_status有publish发布、draft草稿、private隐私状态可选，默认草稿。如果是publish会直接发布
    post.post_status = 'publish'
    # 推送文章到WordPress网站
    wp.call(NewPost(post))
    pass


def uploadImageIfNeed(imageName: str, wp: Client):
    fileName = image_dir_path+imageName
    if not os.path.exists(fileName):
        return None
    imageData = {
        'name': imageName,
        'type': 'image/jpeg',
    }
    with open(fileName, 'rb') as img:
        imageData['bits'] = xmlrpc_client.Binary(img.read())
    response = wp.call(media.UploadFile(imageData))
    thumbnailId = response.get('id', None)
    return thumbnailId


def convertMd2HTML(content: str) -> str:
    post_content_html = markdown.markdown(
        content, output_format='html5', extensions=['extra'])
    return post_content_html


wordpress_xmlrcpath = 'https://blog.1kye.com/xmlrpc.php'
wordpress_user_name = 'YourName'
wordpress_user_passwd = 'Password'
# 缩略图保存的目录
image_dir_path = './md-images/'

if __name__ == "__main__":
    # 获得md文章路径信息
    dir = sys.argv[1]
    print(dir)
    os.makedirs(image_dir_path, exist_ok=True)
    imgNames = []
    for imgname in os.listdir(image_dir_path):
        if not imgname.endswith('.jpg'):
            continue
        imgNames.append(imgname)

    use_thumbnail = len(imgNames) is not 0
    index = 0
    wp = Client(wordpress_xmlrcpath,
                wordpress_user_name, wordpress_user_passwd)
    for i in os.listdir(dir):
        if not i.endswith('.md'):
            continue
        path = dir+"/"+i
        try:
            run(path, imgNames[index] if use_thumbnail else None, wp=wp)
        except:
            print("faild: "+path)
        index += 1
