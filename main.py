import argparse
import os
import time
import re

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathvalidate import sanitize_filename

import url_processing
import parse_tululu_category as parse_genre


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('table').find('h1').text.split('::')[0].strip()
    image_tag = soup.find('table').find('div', class_='bookimage').find('img')['src']
    comments = soup.select('.texts .black')
    genres = soup.select('span.d_book a')
    return {
        'title': title_tag,
        'image': image_tag,
        'comments': [comment.text for comment in comments],
        'genres': [genre.text for genre in genres],
    }


def download_books(start_id, end_id, books_dir, images_dir):
    base_url = 'https://tululu.org'
    for book_id in range(start_id, end_id, 1):
        download_book(base_url, book_id, books_dir, images_dir)


def download_books_genre(genre, books_dir, images_dir):
    base_url = 'https://tululu.org'
    books_dir = os.path.join(books_dir, f'genre_{genre}')
    images_dir = os.path.join(images_dir, f'genre_{genre}')
    os.makedirs(books_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    for page in range(1, 5, 1):
        genre_page_url = f"{base_url}/l{genre}/{page}/"
        soup = parse_genre.get_soup(genre_page_url)
        for book_id in parse_genre.get_book_path(soup):
            book_number = ''.join(filter(lambda x: x.isdigit(), book_id))
            download_book(base_url, book_number, books_dir, images_dir)


def download_book(base_url, book_id, books_dir, images_dir):
    params = {'id': f'{book_id}'}
    try:
        book_response = requests.get(f'{base_url}/txt.php', params)
        book_response.raise_for_status()
        url_processing.check_for_redirect(book_response)
        response = requests.get(f'{base_url}/b{book_id}')
        book_description = parse_book_page(response)
        file_name = sanitize_filename(book_description['title'])
        file_name = f'{os.path.join(books_dir, file_name)}.txt'
        with open(file_name, 'w') as file:
            file.write(book_response.text)
        image_url = f'{base_url}{book_description["image"]}'
        expansion = url_processing.get_file_type(image_url)
        file_name = f'{os.path.join(images_dir, book_description["title"])}.{expansion}'
        url_processing.download_image(image_url, file_name)
    except requests.exceptions.HTTPError as net_error:
        print(f"book_id {book_id}: {net_error}")
    except requests.exceptions.ConnectionError as connect_error:
        print(f"book_id {book_id}: {connect_error}")
        time.sleep(10)


def main():
    load_dotenv()
    books_dir = os.getenv('BOOKS_DIR')
    os.makedirs(books_dir, exist_ok=True)
    images_dir = os.getenv('IMAGES_DIR')
    os.makedirs(images_dir, exist_ok=True)
    # download_books(238, 241, books_dir, images_dir)
    download_books_genre(55, books_dir, images_dir)
    # download_book('https://tululu.org', str('239'), books_dir, images_dir)
    # parser = argparse.ArgumentParser(description='Script download books between ID start and ID end')
    # parser.add_argument('start_id', help='Начальный ID книги', type=int)
    # parser.add_argument('end_id', help='Конечный ID книги', type=int)
    # args = parser.parse_args()
    # download_books(args.start_id, args.end_id, books_dir, images_dir)


if __name__ == '__main__':
    main()
