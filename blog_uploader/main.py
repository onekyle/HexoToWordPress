import os
import sys
import argparse
from blog_uploader.markdown_parser import parse_markdown
from blog_uploader.wordpress_publisher import publish_post

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('md', help='Path to a markdown file or directory with markdown files')
    parser.add_argument('img', default=None, help='Path to an image file or directory with image files')
    args = parser.parse_args()

    # Check if the provided markdown path is a file or a directory
    if os.path.isfile(args.md):
        markdown_files = [args.md]
    elif os.path.isdir(args.md):
        markdown_files = sorted([os.path.join(args.md, f) for f in os.listdir(args.md) if f.endswith('.md')])
    else:
        print("Invalid path provided for markdown file(s).")
        sys.exit()

    image_files = []
    # Check if an image path is provided and if it's a file or a directory
    if args.img:
        if os.path.isfile(args.img):
            image_files = [args.img]
        elif os.path.isdir(args.img):
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # 支持的图片扩展名列表
            image_files = sorted([os.path.join(args.img, f) for f in os.listdir(args.img) if os.path.splitext(f)[1].lower() in image_extensions])
        else:
            print("Invalid path provided for image file(s).")
            sys.exit()
    
    # Iterate over each markdown file
    for i, md_file_path in enumerate(markdown_files):
        post_title, post_tags, post_category, post_date, post_content = parse_markdown(md_file_path)
        
        post_image = None
        if i < len(image_files):
            post_image = image_files[i]
        publish_post(post_title, post_tags, post_category, post_date, post_content, post_image)    
    

if __name__ == "__main__":
    main()