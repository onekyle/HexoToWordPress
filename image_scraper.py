import argparse
import json
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
from urllib.request import urlretrieve

class UnsplashImageScraper:
    def __init__(self, save_dir, style, count):
        self.save_dir = save_dir
        self.style = style
        self.count = count

    def scrape(self):
        url = f'https://unsplash.com/napi/search/photos?query={self.style}&xp=&order_by=latest&per_page={self.count}&page=1'
        response = requests.get(url)
        if response.status_code != 200:
            print('访问失败, 请检查网络')
            return
        html_str = response.content.decode()
        results = json.loads(html_str)["results"]

        with ThreadPoolExecutor(max_workers=5) as executor:
            for r in results:
                urlencode = r['urls']['regular']
                url = unquote(urlencode)
                img_id = r['id']
                save_path = f'{self.save_dir}/{img_id}.jpg'
                executor.submit(self.download_img, url, save_path)

    @staticmethod
    def download_img(url: str, save_path: str):
        try:
            urlretrieve(url, save_path)
            print(f"Downloaded image and saved to {save_path}")
        except Exception as e:
            print(f"Failed to download image from {url}. Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # 添加目录参数
    parser.add_argument('dir', help='存储图片目录')

    # 添加风格参数
    parser.add_argument('-s', '--style', default='landscape', help='下载图片的风格')

    # 添加个数参数
    parser.add_argument('-n', '--count', type=int, default=10, help='批量下载的个数')

    args = parser.parse_args()

    scraper = UnsplashImageScraper(args.dir, args.style, args.count)
    scraper.scrape()