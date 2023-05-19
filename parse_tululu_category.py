import requests
from bs4 import BeautifulSoup


def get_soup(genre_page_url):
    response = requests.get(genre_page_url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


def get_book_path(soup):
    tables = soup.select("table.d_book")
    books_paths = []
    for book in tables:
        books_paths.append(book.find('a')['href'])
    return books_paths
