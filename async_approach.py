import argparse
import asyncio
import aiohttp
import requests
import time
import re

URL = 'https://wallpaperscraft.ru/'


def get_image_urls(url, image_format='jpg', image_amount=5):
    return list(re.findall(r'https:[\S]*\.' + f'{image_format}', requests.get(url).text))[:image_amount]


async def download(url):
    start_time_current = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.read()
            name = re.findall(r".*\/([^\/]+)$", str(url))
            with open(f'{name[0]}', 'wb') as picture:
                picture.write(text)
            print(f'Downloaded for {time.time() - start_time_current:.3f} sec')


async def main(url):
    tasks = []
    for url in get_image_urls(url):
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

def asyn_download(url):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Downloading five images')
    parser.add_argument('url', type=str)
    args=parser.parse_args()
    start_time = time.time()
    asyn_download(args.url)
    print(f"Common downloading time: {time.time() - start_time:.3f} sec")