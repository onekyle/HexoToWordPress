import argparse
from blog_uploader.markdown_parser import parse_markdown
from blog_uploader.wordpress_publisher import publish_post

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="markdown file path or the folder path that contains markdown files")
    parser.add_argument("thumbnail", type=str, nargs='?', help="optional, post thumbnail's path, or the folder path that contains thumbnail files, only support jpg image type")
    args = parser.parse_args()
    
    post_title, post_tags, post_category, post_date, post_content = parse_markdown(args.path)
    publish_post(post_title, post_tags, post_category, post_date, post_content, args.thumbnail)

if __name__ == "__main__":
    main()