import os

def load_env():
    with open(".env") as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

load_env()

WORDPRESS_XMLRCPATH = os.getenv('WORDPRESS_XMLRCPATH')
WORDPRESS_USER_NAME = os.getenv('WORDPRESS_USER_NAME')
WORDPRESS_USER_PASSWD = os.getenv('WORDPRESS_USER_PASSWD')