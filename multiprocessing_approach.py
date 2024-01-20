import argparse

import requests
from multiprocessing import Process
import time
import re

URL = 'https://wallpaperscraft.ru/'

start_time = time.time()


def get_image_urls(url, image_format='jpg', image_amount=5):
    return list(re.findall(r'https:[\S]*\.' + f'{image_format}', requests.get(url).text))[:image_amount]


def download_image_file(url):
    start_time_current = time.time()
    response = requests.get(f'{url}')
    name = re.findall(r".*\/([^\/]+)$", str(url))
    with open(f'{name[0]}', 'wb') as picture:
        picture.write(response.content)
    print(f'Downloaded for {time.time() - start_time_current:.3f} sec')

def multiprocessing_download(url):
    image_url_list = get_image_urls(URL)
    processes = []

    for url in image_url_list:
        process = Process(target=download_image_file, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Downloading five images')
    parser.add_argument('url', type=str)
    args=parser.parse_args()
    print(args)
    start_time = time.time()
    multiprocessing_download(args.url)
    print(f"Common downloading time: {time.time() - start_time:.3f} sec")
