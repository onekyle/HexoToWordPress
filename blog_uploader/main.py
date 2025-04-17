import os
import sys
import argparse
from blog_uploader.markdown_parser import parse_markdown
from blog_uploader.wordpress_publisher import publish_post
from blog_uploader.logger import setup_logger

logger = setup_logger()

def find_markdown_files(directory):
    """递归查找目录下的所有markdown文件"""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return sorted(markdown_files)

def find_image_files(directory):
    """递归查找目录下的所有图片文件"""
    image_files = []
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(os.path.join(root, file))
    return sorted(image_files)

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('md', help='Path to a markdown file or directory with markdown files')
        parser.add_argument('img', nargs='?', default=None, help='Path to an image file or directory with image files')
        args = parser.parse_args()

        logger.info(f"开始处理文件: {args.md}")
        if args.img:
            logger.info(f"图片目录: {args.img}")

        # Check if the provided markdown path is a file or a directory
        if os.path.isfile(args.md):
            markdown_files = [args.md]
            logger.info(f"处理单个文件: {args.md}")
        elif os.path.isdir(args.md):
            markdown_files = find_markdown_files(args.md)
            logger.info(f"处理目录及其子目录中的文件: {len(markdown_files)} 个文件")
        else:
            logger.error(f"无效的路径: {args.md}")
            print("Invalid path provided for markdown file(s).")
            sys.exit()

        image_files = []
        # Check if an image path is provided and if it's a file or a directory
        if args.img:
            if os.path.isfile(args.img):
                image_files = [args.img]
                logger.info(f"处理单个图片: {args.img}")
            elif os.path.isdir(args.img):
                image_files = find_image_files(args.img)
                logger.info(f"处理目录及其子目录中的图片: {len(image_files)} 个文件")
            else:
                logger.error(f"无效的图片路径: {args.img}")
                print("Invalid path provided for image file(s).")
                sys.exit()
        
        # Iterate over each markdown file
        for i, md_file_path in enumerate(markdown_files):
            logger.info(f"处理第 {i+1}/{len(markdown_files)} 个文件: {md_file_path}")
            post_title, post_tags, post_category, post_categories, post_date, post_content, index_img = parse_markdown(md_file_path)
            
            # 优先使用index_img作为特色图片
            post_image = None
            if index_img:
                # 如果index_img是相对路径，转换为绝对路径
                if not os.path.isabs(index_img) and not index_img.startswith(('http://', 'https://')):
                    # 相对于markdown文件所在目录
                    post_image = os.path.join(os.path.dirname(md_file_path), index_img)
                    logger.debug(f"使用相对路径图片: {index_img} -> {post_image}")
                else:
                    post_image = index_img
                    logger.debug(f"使用图片: {post_image}")
            elif i < len(image_files):
                post_image = image_files[i]
                logger.debug(f"使用目录中的图片: {post_image}")
                
            publish_post(post_title, post_tags, post_category, post_categories, post_date, post_content, post_image)
            
        logger.info("所有文件处理完成")
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        raise
    

if __name__ == "__main__":
    main()