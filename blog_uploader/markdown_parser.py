import markdown
import frontmatter
import datetime

def parse_markdown(path):
    post = frontmatter.load(path)
    post_title = post.metadata.get('title', None)
    post_tags = post.metadata.get('tags', None)
    post_category = post.metadata.get('category', None)
    date = post.metadata.get('date', datetime.datetime.today())
    post_date = date
    post_content = convert_md2html(post.content)
    return post_title, post_tags, post_category, post_date, post_content

def convert_md2html(content):
    return markdown.markdown(content, output_format='html5', extensions=['extra'])