
import os
import requests
import url_processing

from pathvalidate import sanitize_filename


from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin


def get_book_title(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('body').find('table').find('td', class_='ow_px_td').find('div').find('h1').text
    title_tag = title_tag.split('::')[0].strip()
    image_tag = soup.find('body').find('table').find('td', class_='ow_px_td').\
        find('div', class_='bookimage').find('a').find('img')['src']
    return {
        'title': title_tag,
        'image': image_tag,
    }


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    if soup.select_one('h1'):
        title, author = soup.select_one('h1').text.split('::')
        img_src = urljoin(response.url, soup.select_one('.bookimage img')['src'])
        comments = soup.select('.texts .black')
        genres = soup.select('span.d_book a')
        return {
            'title': title.strip(),
            'author': author.strip(),
            'img': img_src,
            'comments': [comment.text for comment in comments],
            'genres': [genre.text for genre in genres]
        }


def main():
    base_url = 'https://tululu.org'
    load_dotenv()
    os.getenv('DEBUG')
    books_dir = os.getenv('BOOKS_DIR')
    images_dir = os.getenv('IMAGES_DIR')
    os.makedirs(books_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    for book_id in range(1, 10, 1):
        book_url = f'{base_url}/txt.php?id=321{book_id}'
        book_title = get_book_title(f'{base_url}/b{book_id}')
        image_url = f'{base_url}/shots/{book_title["image"]}'
        try:
            file_name = sanitize_filename(book_title['title'])
            file_name = f'{os.path.join(books_dir, file_name)}.txt'
            url_processing.download_txt(book_url, file_name)
            expansion = url_processing.get_file_type(image_url)
            file_name = f'{os.path.join(books_dir, book_title["title"])}.{expansion}'
            url_processing.download_image(image_url, file_name)
        except requests.exceptions.HTTPError as net_error:
            print(f"book_id {book_id}: {net_error}")
        except IndexError:
            print(f"Unable to create a book {book_title['title']}, it doesn't exist!")


if __name__ == '__main__':
    main()


