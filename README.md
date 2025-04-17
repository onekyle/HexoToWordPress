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
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── main.py
│   ├── markdown_parser.py
│   └── wordpress_publisher.py
└── image_scraper.py
```

## Markdown file format
Before use this script, you should make sure your post was created by hexo command or it has a hexo post format:
```markdown
---
title: Your post title
date: 2021-04-01 20:16:49
tags: [Python]
categories: [技术, 编程]  # 支持多个分类
index_img: https://example.com/image.jpg  # 支持网络图片链接
---

...content...
```

## Features
- 支持单个文件或目录批量上传
- 支持递归处理目录下的所有子文件夹
- 支持文章特色图片（支持本地图片和网络图片）
- 支持多个分类
- 详细的日志记录
- 自动处理图片格式（jpg、jpeg、png、gif、webp）

## Usage
### 1. 安装依赖
```bash
pip install python-wordpress-xmlrpc python-frontmatter requests
```

### 2. 配置WordPress信息
编辑 `.env` 文件，填入你的 WordPress 信息：
```
WORDPRESS_XMLRCPATH=https://your-blog.com/xmlrpc.php
WORDPRESS_USER_NAME=YourName
WORDPRESS_USER_PASSWD=Password
```

### 3. 上传博客
#### 上传单个文件
```bash
python -m blog_uploader.main path/to/your/post.md
```

#### 上传目录下的所有文件（包括子文件夹）
```bash
python -m blog_uploader.main path/to/posts/directory
```

#### 上传带图片的文章
```bash
python -m blog_uploader.main path/to/your/post.md path/to/images/directory
```

### 4. 日志查看
- 日志文件保存在 `logs` 目录下
- 文件名格式：`blog_uploader_YYYYMMDD.log`
- 同时输出到控制台和文件

## 目录结构
你可以按照以下方式组织你的文件：
```
posts/
├── 分类1/
│   ├── 文章1.md
│   ├── 文章2.md
│   └── images/
│       ├── 图片1.jpg
│       └── 图片2.png
├── 分类2/
│   ├── 文章3.md
│   └── images/
│       └── 图片3.jpg
└── 其他文章.md
```

## 图片处理
1. 优先使用文章中的 `index_img` 字段作为特色图片
2. 如果 `index_img` 是网络链接，会自动下载并上传
3. 如果 `index_img` 是相对路径，会自动转换为绝对路径（相对于markdown文件所在目录）
4. 如果没有 `index_img`，会使用指定的图片目录中的图片

## 分类处理
1. 同时支持 `category` 和 `categories` 字段
2. 如果两个字段都存在，会合并使用
3. 支持单个分类和多个分类

## 注意事项
1. 确保 markdown 文件格式正确
2. 确保 WordPress 信息配置正确
3. 网络图片下载需要网络连接
4. 图片上传需要 WordPress 有足够的权限
5. 相对路径的图片会相对于markdown文件所在目录进行解析 