import os
from urllib.parse import urlparse

import requests


def download_image(url, file_name, payload=None):
    response = requests.get(url, payload)
    response.raise_for_status()
    with open(file_name, 'wb') as file:
        file.write(response.content)


def get_file_type(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip("/").split("/")[-1]
    return os.path.splitext(path)[1][1:]


def check_for_redirect(response):
    if len(response.history) > 1:
        raise requests.exceptions.HTTPError('redirect')
