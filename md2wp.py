# coding=utf-8
'''
@Author: Kyle
@Date: 2020-03-05 08:34:04
LastEditors: Kyle
LastEditTime: 2023-05-21 21:40:11
@Description: 
FilePath: /HexoToWordPress/md2wp.py
'''
import sys
import argparse
import markdown
import frontmatter
import datetime
import logging
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import os
import re
from urllib.request import urlretrieve
import threading
from enum import IntEnum


def load_env():
    with open(".env") as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

load_env()

# 配置你自己的地址 账号密码
wordpress_xmlrcpath: str = os.getenv('WORDPRESS_XMLRCPATH')
wordpress_user_name: str = os.getenv('WORDPRESS_USERNAME')
wordpress_user_passwd: str = os.getenv('WORDPRESS_PASSWORD')

image_dir_path: str = None

class ThumbnailAddMode(IntEnum):
    NONE = 0
    SINGLE = 1
    FILESMATCH = 2

def run(path: str, imgname: str, wp: Client, image_dir_path):
    logging.info('start: %s' % path)
    post = frontmatter.load(path)

    # extract the post metadata
    post_title = post.metadata.get('title', None)
    post_tags = post.metadata.get('tags', None)
    post_category = post.metadata.get('category', None)
    date = post.metadata.get('date', datetime.datetime.today())
    post_date = date
    post_content = post.content

    # convert markdown to html
    post_content_html = convertMd2HTML(post_content)

    # create a new wordpress post
    wp_post = WordPressPost()
    wp_post.title = post_title
    wp_post.date = post_date
    wp_post.thumbnail = uploadImageIfNeed(imgname, wp, image_dir_path)

    logging.info("上传图片成功. id=" + wp_post.thumbnail)
    wp_post.content = post_content_html
    terms_names = {'post_tag': post_tags, 'category': post_category}
    wp_post.terms_names = terms_names
    wp_post.post_status = 'publish'

    # publish the post
    wp.call(NewPost(wp_post))

def uploadImageIfNeed(imageName: str, wp: Client, image_dir_path: str):
    if imageName is None or image_dir_path is None:
        return None
    fileName = os.path.join(image_dir_path, imageName)
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


def thumbnailImgNameForIndex(index: int, imgNames: list, image_mode: ThumbnailAddMode):
    if image_mode == ThumbnailAddMode.NONE:
        return None
    elif image_mode == ThumbnailAddMode.SINGLE:
        return imgNames[0]
    else:
        return imgNames[index]


def setup_image(args_img_path: str):
    imgNames = []
    image_dir_path = None
    if args_img_path is None:
        image_mode = ThumbnailAddMode.NONE
    elif os.path.isdir(args_img_path):
        image_dir_path = args_img_path
        file_list = [f for f in os.listdir(args_img_path) if f.endswith('.jpg')]
        imgNames = sorted(file_list)
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
            logging.warning("Single thumbnail image file type error, will not upload")
    else:
        raise ValueError(f"Invalid thumbnail argument: {args_img_path}")
    return image_mode, image_dir_path, imgNames

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, help="markdown file path or the folder path that contains markdown files")
    parser.add_argument("thumbnai", type=str, nargs='?',
                        help="optional, post thumbnail's path, or the folder path that contains thumbnail files, only support jpg image type")
    pargs = parser.parse_args()

    args_path = pargs.path
    useModeAll = os.path.isdir(args_path)
    args_img_path = pargs.thumbnai

    image_mode, image_dir_path, imgNames = setup_image(args_img_path)

    if image_mode == ThumbnailAddMode.FILESMATCH and not useModeAll:
        raise ValueError(
            "use wrong thumbnail path, please specify which thumbnail path to use")

    logging.info(f"args_path: {args_path}, args_img_path: {args_img_path}, image_dir_path: {image_dir_path}, imgMode: {image_mode}, imgNames: {imgNames}")

    if useModeAll:
        md_filespaths = os.listdir(args_path)
    else:
        md_filespaths = [os.path.basename(args_path)]
        args_path = os.path.dirname(args_path)

    wp = Client(wordpress_xmlrcpath, wordpress_user_name, wordpress_user_passwd)
    for index, md_file in enumerate(md_filespaths):
        if not md_file.endswith('.md'):
            continue
        path = os.path.join(args_path, md_file)
        try:
            run(path, thumbnailImgNameForIndex(index, imgNames, image_mode), wp, image_dir_path)
        except Exception as err:
            logging.error("Failed to upload post with path: "+path, err)

