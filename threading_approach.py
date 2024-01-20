import argparse

import requests
import time
import re
import threading

URL = 'https://wallpaperscraft.ru/'


def get_image_urls(url, image_format='jpg', image_amount=5):
    return list(re.findall(r'https:[\S]*\.' + f'{image_format}', requests.get(url).text))[:image_amount]


def download_image_file(url):
    start_time_current = time.time()
    response = requests.get(f'{url}')
    name = re.findall(r".*\/([^\/]+)$", str(url))
    with open(f'{name[0]}', 'wb') as picture:
        picture.write(response.content)
    print(f'Downloaded for {time.time() - start_time_current:.3f} sec')


def threading_download(URL):
    threads = []
    image_url_list = get_image_urls(URL)

    for url in image_url_list:
        thread = threading.Thread(target=download_image_file, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Downloading five images')
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    start_time = time.time()
    threading_download(args.url)
    print(f"Common downloading time: {time.time() - start_time:.3f} sec")
