import requests
from bs4 import BeautifulSoup

import url_processing


def get_soup(genre_page_url):
    response = requests.get(genre_page_url)
    response.raise_for_status()
    url_processing.check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def get_books_paths(soup):
    paths = soup.select("table.d_book")
    books_paths = []
    for path in paths:
        books_paths.append(path.find('a')['href'])
    return books_paths
