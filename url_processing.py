import requests
import os

from urllib.parse import urlparse


def download_image(url, file_name, payload=None):
    response = requests.get(url, payload)
    response.raise_for_status()
    with open(file_name, 'wb') as file:
        file.write(response.content)


def get_file_type(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip("/").split("/")[-1]
    return os.path.splitext(path)[1][1:]


def download_txt(book_url, file_name):
    response = requests.get(book_url)
    response.raise_for_status()
    with open(file_name, 'w') as file:
        file.write(response.text)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError(response.history[0])
