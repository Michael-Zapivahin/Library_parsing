from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def get_soup(genre_page_url):
    response = requests.get(genre_page_url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


def get_book_path(soup):
    tables = soup.find_all('table', class_='d_book')
    books = []
    for book in tables:
        books.append(book.find('a')['href'])
    return books



def main():
    url = "https://tululu.org/"
    genre = 55
    for page in range(1, 10, 1):
        genre_page_url = f"{url}l{genre}/{page}/"
        soup = get_soup(genre_page_url)
        books_paths = get_book_path(soup)
        books_url = [urljoin(url, path) for path in books_paths]
        print(books_url)


if __name__ == '__main__':
    main()
