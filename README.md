# HexoToWordPress

Convert your hexo markdown posts to html then publish to your wordpress blog.

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

install python-wordpress-xmlrpc
```
pip install python-wordpress-xmlrpc
```
read the [python-wordpress-xmlrpc doc](https://python-wordpress-xmlrpc.readthedocs.io/en/latest/) to get the your wordpress xmlrcpath.

fill your xmlrcpath, user name and passwd in md2wp.py.

```
wordpress_xmlrcpath: str = 'https://blog.1kye.com/xmlrpc.php'
wordpress_user_name: str = 'YourName'
wordpress_user_passwd: str = 'Password'
```

then you can upload your post to your wordpress blog.

upload single hexo post
```
python3 md2wp.py markdown_file
```

upload whole hexo post folder
```
python3 md2wp.py YourHexoPath/source/_posts
```


```
usage: md2wp.py [-h] path [thumbnai]

positional arguments:
  path        markdown file path or the folder path that contains markdown
              files
  thumbnai    optional, post thumbnail's path, or the folder path that contains
              thumbnail files, only support jpg image type

optional arguments:
  -h, --help  show this help message and exit
```
## 如果你在天朝
[从Hexo迁移到WordPress](https://blog.1kye.com/2020/03/28/%e4%bb%8ehexo%e8%bf%81%e7%a7%bb%e5%88%b0wordpress/)