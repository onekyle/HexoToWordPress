# coding=utf-8
'''
@Author: Kyle
@Date: 2020-03-06 13:57:33
LastEditors: Kyle
LastEditTime: 2023-05-21 19:18:20
@Description: 
FilePath: /HexoToWordPress/unsplash_crawler.py
'''

import sys
import requests
import argparse
import json
from urllib.parse import unquote
from urllib.request import urlretrieve
import threading

# https://unsplash.com/s/photos/landscape?order_by=latest&per_page=50
# https://unsplash.com/napi/search/photos?query=landscape&xp=&per_page=20&page=3&order_by=latest


def run(key: str):
    url = f'https://unsplash.com/napi/search/photos?query={key}&xp=&order_by=latest&per_page={count}&page=1'
    reponse = requests.get(url)
    if reponse.status_code != 200:
        print('访问失败, 请检查网络')
        return
    html_str = reponse.content.decode()
    results = json.loads(html_str)["results"]
    # ['results']
    # imgurls = []
    for r in results:
        urlencode = r['urls']['regular']
        url = unquote(urlencode)
        img_id = r['id']
        save_path = f'{image_dir_path}/{img_id}.jpg'
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
    parser = argparse.ArgumentParser()

    # 添加目录参数
    parser.add_argument('dir', help='存储图片目录')

    # 添加风格参数
    parser.add_argument('-s', '--style', default='landscape', help='下载图片的风格')

    # 添加个数参数
    parser.add_argument('-n', '--count', type=int, default=10, help='批量下载的个数')

    args = parser.parse_args()

    image_dir_path = args.dir
    count = args.count
    run(args.style)
