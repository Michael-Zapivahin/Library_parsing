import argparse
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathvalidate import sanitize_filename

import url_processing


def parse_book_page(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
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


def download_books(start_id, end_id):
    base_url = 'https://tululu.org'
    load_dotenv()
    books_dir = os.getenv('BOOKS_DIR')
    images_dir = os.getenv('IMAGES_DIR')
    os.makedirs(books_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    for book_id in range(start_id, end_id, 1):
        params = {'id': f'321{book_id}'}
        book_url = f'{base_url}/txt.php'
        book_title = parse_book_page(f'{base_url}/b{book_id}')
        try:
            file_name = sanitize_filename(book_title['title'])
            file_name = f'{os.path.join(books_dir, file_name)}.txt'
            url_processing.download_txt(book_url, file_name, params)
            if book_title["image"]:
                image_url = f'{base_url}{book_title["image"]}'
                expansion = url_processing.get_file_type(image_url)
                file_name = f'{os.path.join(images_dir, book_title["title"])}.{expansion}'
                url_processing.download_image(image_url, file_name)
        except requests.exceptions.HTTPError as net_error:
            print(f"book_id {book_id}: {net_error}")
        except IndexError:
            print(f"Unable to create a book {book_title['title']}, it doesn't exist!")


def main():
    parser = argparse.ArgumentParser(description='Script download books between ID start and ID end')
    parser.add_argument('start_id', help='Начальный ID книги', type=int)
    parser.add_argument('end_id', help='Конечный ID книги', type=int)
    args = parser.parse_args()
    download_books(args.start_id, args.end_id)


if __name__ == '__main__':
    main()
