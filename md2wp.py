# coding=utf-8
'''
@Author: Kyle
@Date: 2020-03-05 08:34:04
LastEditors: Kyle
LastEditTime: 2021-04-01 21:27:55
@Description: 
FilePath: /MarkdownToWordPress/md2wp.py
'''

import sys
import argparse
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
from enum import IntEnum

# 配置你自己的地址 账号密码
wordpress_xmlrcpath: str = None  # 'https://blog.1kye.com/xmlrpc.php'
wordpress_user_name: str = None  # 'YourName'
wordpress_user_passwd: str = None  # 'Password'

image_dir_path: str = None


class ThumbnailAddMode(IntEnum):
    NONE = 0
    SINGLE = 1
    FILESMATCH = 2


def run(path: str, imgname: str, wp: Client):
    print('start: %s' % path)
    post = frontmatter.load(path)
    # 将获取到的信息赋值给变量
    # print(post.metadata)
    post_title = post.metadata.get('title', None)

    post_tags = post.metadata.get('tags', None)
    post_category = post.metadata.get('category', None)
    date = post.metadata.get('date', datetime.datetime.today())
    post_date = date
    post_content = post.content

    # convert
    post_content_html = convertMd2HTML(post_content)

    # publish
    post = WordPressPost()
    post.title = post_title
    post.date = post_date

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
    if imageName is None or image_dir_path is None:
        return None
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


def thumbnailImgNameForIndex(index: int) -> str:
    if image_mode == ThumbnailAddMode.NONE:
        return None
    elif image_mode == ThumbnailAddMode.SINGLE:
        return imgNames[0]
    else:
        return imgNames[index]


if __name__ == "__main__":
    global args_img_path
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, help="markdown file path or the folder path that contains markdown files")

    parser.add_argument("thumbnai", type=str, nargs='?',
                        help="optional, post thumbnail's path, or the folder path that contains thumbnail files, only support jpg image type")
    pargs = parser.parse_args()

    if wordpress_xmlrcpath is None or wordpress_user_name is None or wordpress_user_passwd is None:
        raise ValueError("please set yourself wordpress configuration items")

    args_path = pargs.path
    useModeAll = os.path.isdir(args_path)

    args_img_path = None
    imgNames = []

    # 图片资源模式判断, 并获取相应所需 imgName
    if args_img_path is None:
        image_mode = ThumbnailAddMode.NONE
    elif os.path.isdir(args_img_path):
        image_dir_path = os.path.dirname(args_img_path)
        img_files = os.listdir(args_img_path)
        img_files.sort(key=lambda x: int(x[:-4]))
        for imgname in img_files:
            if not imgname.endswith('.jpg'):
                continue
            imgNames.append(imgname)
        if len(imgNames) == 0:
            image_mode = ThumbnailAddMode.NONE
        elif len(imgNames) == 1:
            image_mode = ThumbnailAddMode.SINGLE
        else:
            image_mode = ThumbnailAddMode.FILESMATCH
    elif os.path.isfile(args_img_path):
        image_dir_path = os.path.dirname(args_img_path)
        if args_img_path.endswith('.jpg'):
            image_mode = ThumbnailAddMode.SINGLE
            imgNames.append(os.path.basename(args_img_path))
        else:
            image_mode = ThumbnailAddMode.NONE
            print("-WARNGIN, single thumbnail image file type error, will not upload")

    if image_mode == ThumbnailAddMode.FILESMATCH and not useModeAll:
        raise ValueError(
            "use wrong thumbnail path, please specify which thumbnail path to use")

    # print(f"args_path: {args_path}, args_img_path: {args_img_path}, image_dir_path: {image_dir_path}, imgMode: {image_mode}, imgNames: {imgNames}")
    
    # markdown 当前模式判断
    if useModeAll:
        md_filespaths = os.listdir(args_path)
    else:
        md_filespaths = [os.path.basename(args_path)]
        args_path = os.path.dirname(args_path)

    
    wp = Client(wordpress_xmlrcpath, wordpress_user_name,
                wordpress_user_passwd)
    index = 0
    for i in md_filespaths:
        if not i.endswith('.md'):
            continue
        path = os.path.join(args_path, i)
        try:
            run(path, thumbnailImgNameForIndex(i), wp=wp)
        except Exception as err:
            print(err)
            print("-ERROR faild upload post with path: "+path)
        index += 1
