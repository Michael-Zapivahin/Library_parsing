
import os
import requests
import url_processing


from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin


def get_book_title(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('body').find('table').find('td', class_='ow_px_td').find('div').find('h1').text
    title_tag = title_tag.split('   ::   ')
    title_tag[0].strip()
    title_tag[1].strip()
    return title_tag[0]


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
    load_dotenv()
    os.getenv('DEBUG')
    media_dir = os.getenv('MEDIA_DIR')
    os.makedirs(media_dir, exist_ok=True)
    for book_id in range(68, 69, 1):
        book_url = f'https://tululu.org/txt.php?id=321{book_id}'
        page_url = f'https://tululu.org/b{book_id}'
        file_name = get_book_title(page_url)
        try:
            url_processing.download_txt(book_url, file_name, book_id)
        except requests.exceptions.HTTPError as err:
            print(f"book_id {book_id}: {err}")
        except IndexError:
            print(f"Can't create book {file_name}, it does not exist!")


if __name__ == '__main__':
    main()


