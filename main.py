import argparse
import os
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathvalidate import sanitize_filename

import url_processing


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('table').find('h1').text.split('::')[0].strip()
    try:
        image_tag = soup.find('table').find('div', class_='bookimage').find('img')['src']
    except AttributeError:
        image_tag = None
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
    os.makedirs(books_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    for book_id in range(start_id, end_id, 1):
        params = {'id': f'321{book_id}'}
        book_url = f'{base_url}/txt.php'
        try:
            response = requests.get(f'{base_url}/b{book_id}')
            response.raise_for_status()
            url_processing.check_for_redirect(response)
            book_description = parse_book_page(response)
            file_name = sanitize_filename(book_description['title'])
            file_name = f'{os.path.join(books_dir, file_name)}.txt'
            url_processing.download_txt(book_url, file_name, params)
            if book_description["image"]:
                image_url = f'{base_url}{book_description["image"]}'
                expansion = url_processing.get_file_type(image_url)
                file_name = f'{os.path.join(images_dir, book_description["title"])}.{expansion}'
                url_processing.download_image(image_url, file_name)
        except requests.exceptions.HTTPError as net_error:
            print(f"book_id {book_id}: {net_error}")
        except AttributeError:
            print(f"The book  {book_description['title']} hasn't the image.")
        except requests.exceptions.ConnectionError as connect_error:
            print(f"book_id {book_id}: {connect_error}")
            time.sleep(10)


def main():
    load_dotenv()
    books_dir = os.getenv('BOOKS_DIR')
    images_dir = os.getenv('IMAGES_DIR')
    parser = argparse.ArgumentParser(description='Script download books between ID start and ID end')
    parser.add_argument('start_id', help='Начальный ID книги', type=int)
    parser.add_argument('end_id', help='Конечный ID книги', type=int)
    args = parser.parse_args()
    download_books(args.start_id, args.end_id, books_dir, images_dir)


if __name__ == '__main__':
    main()
