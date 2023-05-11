import requests
import os

from urllib.parse import urlparse
from pathvalidate import sanitize_filename


def get_file_type(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip("/").split("/")[-1]
    return os.path.splitext(path)[1][1:]


def download_txt(book_url, file_name, folder='books/'):
    response = requests.get(book_url)
    response.raise_for_status()
    file_name = sanitize_filename(file_name)
    os.makedirs(folder, exist_ok=True)
    with open(f'{os.path.join(folder, file_name)}.txt', 'w') as file:
        file.write(response.text)
    return(f'{os.path.join(folder, file_name)}.txt')


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError(response.history[0])
