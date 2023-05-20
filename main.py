import argparse
import os
import time
import pickle

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


def download_books_genre(genre, books_dir, images_dir, comments_dir, start_page, end_page, download_params):
    base_url = 'https://tululu.org'
    books_dir = os.path.join(books_dir, f'genre_{genre}')
    images_dir = os.path.join(images_dir, f'genre_{genre}')
    comments_dir = os.path.join(comments_dir, f'genre_{genre}')
    os.makedirs(books_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(comments_dir, exist_ok=True)
    for page in range(start_page, end_page+1, 1):
        genre_page_url = f"{base_url}/l{genre}/{page}/"
        soup = parse_genre.get_soup(genre_page_url)
        for book_id in parse_genre.get_book_path(soup):
            book_number = ''.join(filter(lambda x: x.isdigit(), book_id))
            download_book(base_url, book_number, books_dir, images_dir, comments_dir, download_params)


def download_book(base_url, book_id, books_dir, images_dir, comments_dir, download_params):
    params = {'id': f'{book_id}'}
    try:
        book_response = requests.get(f'{base_url}/txt.php', params)
        book_response.raise_for_status()
        url_processing.check_for_redirect(book_response)
        response = requests.get(f'{base_url}/b{book_id}')
        book_description = parse_book_page(response)
        if not download_params['skip_txt']:
            file_name = sanitize_filename(book_description['title'])
            if download_params['root_dir']:
                books_dir = os.path.join(download_params['root_dir'], books_dir)
            file_name = f'{os.path.join(books_dir, file_name)}.txt'
            save_comments(comments_dir, book_description, download_params)
            with open(file_name, 'w') as file:
                file.write(book_response.text)
        if not download_params['skip_img']:
            image_url = f'{base_url}/{book_description["image"]}'
            expansion = url_processing.get_file_type(image_url)
            if download_params['root_dir']:
                images_dir = os.path.join(download_params['root_dir'], images_dir)
            file_name = f'{os.path.join(images_dir, book_description["title"])}.{expansion}'
            url_processing.download_image(image_url, file_name)
    except requests.exceptions.HTTPError as net_error:
        print(f"book_id {book_id}: {net_error}")
    except requests.exceptions.ConnectionError as connect_error:
        print(f"book_id {book_id}: {connect_error}")
        time.sleep(10)


def save_comments(comments_dir, description, download_params):
    book_description = {
        'Title: ': description['title'],
        'Autor: ': description['author'],
        'Genre: ': description['genre'],
        'Comments: ': description['comments'],
    }
    if download_params['root_dir']:
        file_name = download_params['root_dir']
    elif download_params['json_path']:
        file_name = download_params['json_path']
    else:
        file_name = comments_dir
    file_name = f'{os.path.join(file_name, description["title"])}.txt'
    with open(file_name, 'wb') as file:
        pickle.dump(book_description, file)


def main():
    load_dotenv()
    books_dir = os.getenv('BOOKS_DIR')
    os.makedirs(books_dir, exist_ok=True)
    images_dir = os.getenv('IMAGES_DIR')
    os.makedirs(images_dir, exist_ok=True)
    comments_dir = os.getenv('COMMENTS')
    os.makedirs(comments_dir, exist_ok=True)
    parser = argparse.ArgumentParser(description='Script download books')
    parser.add_argument('-s', '--start_page', help='first page id (default: 1)', type=int, default=1)
    parser.add_argument('-e', '--end_page', help='last page id (default: 0)', type=int, default=0)
    parser.add_argument('--skip_img', default=False, help='Turn off images download', type=bool)
    parser.add_argument('--skip_txt', default=False, help='Turn off texts download', type=bool)
    parser.add_argument('--root_dir', default='', help='Destination folder path', type=str)
    parser.add_argument('--json_path', default='', help='JSON folder path', type=str)
    args = parser.parse_args()
    start_id = args.start_page
    end_id = args.end_page
    download_params = {
        'root_dir': args.root_dir,
        'json_path': args.json_path,
        'skip_img': args.skip_img,
        'skip_txt': args.skip_txt,
    }
    base_url = 'https://tululu.org'
    genre_id = 55
    if end_id == 0:
        genre_page_url = f"{base_url}/l{genre_id}"
        soup = parse_genre.get_soup(genre_page_url)
        end_id = int(soup.select_one('body table p.center').contents[-1].text)
    if start_id < end_id:
        download_books_genre(
            genre_id,
            books_dir,
            images_dir,
            comments_dir,
            start_id,
            end_id,
            download_params
        )


if __name__ == '__main__':
    main()
