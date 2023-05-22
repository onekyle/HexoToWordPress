# HexoToWordPress ![python3.7](https://img.shields.io/badge/python-3.7-blue)

Convert your hexo markdown posts to html then publish to your wordpress blog.

## 中文
[从Hexo迁移到WordPress](https://blog.1kye.com/277)

## Project file structure
```zsh
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── blog_uploader
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── markdown_parser.py
│   └── wordpress_publisher.py
└── image_scraper.py
```

## Markdown file format
Before use this script, you should make sure your post was created by hexo command or it has a hexo post format:
```markdown
---
title: Your post title
date: 2021-04-01 20:16:49
tags: [Python]
---

...content...
```

## Usage
### upload blog

install python-wordpress-xmlrpc
```python
pip install python-wordpress-xmlrpc
```
read the [python-wordpress-xmlrpc doc](https://python-wordpress-xmlrpc.readthedocs.io/en/latest/) to get the your wordpress xmlrcpath.

fill your xmlrcpath, user name and passwd in .env.

```
WORDPRESS_XMLRCPATH=https://blog.1kye.com/xmlrpc.php
WORDPRESS_USER_NAME=YourName
WORDPRESS_USER_PASSWD=Password
```

then you can upload your post to your wordpress blog.

```python
python -m blog_uploader.main file
```

### upload blog with image
#### download images
```zsh
usage: image_scraper.py [-h] [-s STYLE] [-n COUNT] dir

positional arguments:
  dir                   存储图片目录

optional arguments:
  -h, --help            show this help message and exit
  -s STYLE, --style STYLE
                        下载图片的风格
  -n COUNT, --count COUNT
                        批量下载的个数
```
```python
python image_scraper.py imgs -s code -n 10
```

#### upload blog 
```python
python -m blog_uploader.main mds imgs
```
