# coding=utf-8
'''
@Author: Kyle
@Date: 2020-03-06 13:57:33
@LastEditors: Kyle
@LastEditTime: 2020-03-28 01:34:26
@Description: 
@FilePath: /MarkdownToWordPress/unsplash_crawler.py
'''

import sys
import requests
import json
from urllib.parse import unquote
from urllib.request import urlretrieve
import threading

# https://unsplash.com/s/photos/landscape?order_by=latest&per_page=50
# https://unsplash.com/napi/search/photos?query=landscape&xp=&per_page=20&page=3&order_by=latest


def run(key: str):
    url = 'https://unsplash.com/napi/search/photos?query=' + \
        key + '&xp=&order_by=latest&per_page=29&page=1'
    reponse = requests.get(url)
    if reponse.status_code != 200:
        print('访问失败, 请检查网络')
        return
    html_str = reponse.content.decode()
    results = json.loads(html_str)['results']
    # imgurls = []
    for r in results:
        urlencode = r['urls']['regular']
        url = unquote(urlencode)
        img_id = r['id']
        save_path = image_dir_path + "/" + img_id
        # imgurls.append(url)
        download_thead = threading.Thread(
            target=downlaodImg, args=(url, save_path,))
        download_thead.run()


def downlaodImg(url: str, save_path: str) -> str:
    ret = urlretrieve(url, save_path)
    if len(ret) == 0:
        return None
    return ret[0]


if __name__ == "__main__":
    global image_dir_path
    image_dir_path = sys.argv[1]
    run('landscape')
