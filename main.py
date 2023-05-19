import argparse
import os
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathvalidate import sanitize_filename

import url_processing
import parse_tululu_category as parse_genre


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.select_one("table.tabs h1")
    raw_title, raw_author = title_tag.text.split("::")
    title = raw_title.strip()
    author = raw_author.strip()
    image = soup.select_one('body div.bookimage img')['src']
    comments = soup.select('.texts .black')
    comments = [comment.text for comment in comments]
    genres_tags = soup.select("span.d_book a")
    genres = [tag.text for tag in genres_tags]
    return {
        'title': title,
        'author': author,
        'image': image,
        'comments': comments,
        'genres': genres,
    }


def download_books(start_id, end_id, books_dir, images_dir):
    base_url = 'https://tululu.org'
    for book_id in range(start_id, end_id, 1):
        download_book(base_url, book_id, books_dir, images_dir)


def download_books_genre(genre, books_dir, images_dir, comments_dir, start_page, end_page):
    base_url = 'https://tululu.org'
    books_dir = os.path.join(books_dir, f'genre_{genre}')
    images_dir = os.path.join(images_dir, f'genre_{genre}')
    os.makedirs(books_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(comments_dir, exist_ok=True)
    for page in range(start_page, end_page+1, 1):
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
        image_url = f'{base_url}/{book_description["image"]}'
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
    comments_dir = os.getenv('COMMENTS')
    os.makedirs(comments_dir, exist_ok=True)
    parser = argparse.ArgumentParser(description='Script download books')
    parser.add_argument('-s', '--start_id', help='first book id (default: 1)', type=int, default=1)
    parser.add_argument('-e', '--end_id', help='last book id (default: 0)', type=int, default=1)
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id
    if end_id == 0:
        base_url = 'https://tululu.org'
        genre_page_url = f"{base_url}/l{55}"
        soup = parse_genre.get_soup(genre_page_url)
        end_id = int(soup.select_one('body table p.center').contents[-1].text)
    if start_id < end_id:
        download_books_genre(55, books_dir, images_dir, comments_dir, start_id, end_id)


if __name__ == '__main__':
    main()
