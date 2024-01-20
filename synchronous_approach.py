import requests
import re
import os
import time
import argparse

URL = 'https://wallpaperscraft.ru/'

def download_files(url):
    start_time = time.time()

    response = requests.get(url)
    result = response.text
    print(response.text.count('jpg'))
    png_List = list(re.findall(r'https:[\S]*\.jpg', result))

    for i, png in enumerate(png_List[:5]):
        start_time_current = time.time()
        response = requests.get(f'{png}')
        name = re.findall(r".*\/([^\/]+)$", str(png))

        with open(f'{name[0]}', 'wb') as picture:
            picture.write(response.content)
        print(f'Downloaded for {time.time() - start_time_current:.5f} sec')

    print(f'Downloaded for {time.time() - start_time:.2f} sec')
    question = input("Would you like to delete downloaded files? Press 1 to delete, any to save ")
    delete_files('.jpg') if question=='1' else None


def delete_files(*args):
    for image in os.listdir(os.getcwd()):
        if image[-4:] in args:
            os.remove(image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Downloading five images')
    parser.add_argument('url', type=str)
    args=parser.parse_args()
    print(args)
    download_files(args.url)
