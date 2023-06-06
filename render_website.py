import json
import os
import urllib.parse

from more_itertools import chunked, sliced
from livereload import Server
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape


DESCRIPTION_DIR = 'media/descriptions'
IMAGES_DIR = 'media/images'


def on_reload():
    os.makedirs('pages', exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template(os.path.join('templates', 'template.html'))
    books_for_page = 10
    columns_count = 2
    genre_id = '55'

    descriptions_dir = os.path.join(DESCRIPTION_DIR, f'genre_{genre_id}')
    file_name = os.path.join(descriptions_dir, 'descriptions.json')
    with open(file_name, 'r', encoding='utf-8') as file:
        book_comments = json.load(file)

    image_dir = os.path.join(IMAGES_DIR, 'genre_55')
    book_descriptions = []
    for book_id, book_description in book_comments.items():
        image_path = book_description['image'].split('/')
        image_file = os.path.join(image_dir, f'book_{image_path[-1]}')
        book_description['image'] = image_file
        book_description['book_id'] = book_id
        book_description['genre'] = genre_id
        book_url = urllib.parse.quote(f'../media/books/genre_{genre_id}/book_{book_id}.txt', safe='/')
        book_description['book_url'] = book_url
        book_descriptions.append(book_description)

    pages = list(sliced(book_descriptions, books_for_page))
    pages_count = len(pages)
    for index, page_books in enumerate(pages, start=1):
        page_columns = list(chunked(page_books, columns_count))
        rendered_page = template.render(
            page_columns=page_columns,
            max_page_num=pages_count,
            page_num=index,
            current_page_num=index,
        )
        with open(os.path.join('pages', f'index{index}.html'), 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    load_dotenv()
    DESCRIPTION_DIR = os.getenv('DESCRIPTION_DIR', default=os.path.join('media', 'descriptions'))
    os.makedirs(DESCRIPTION_DIR, exist_ok=True)
    IMAGES_DIR = os.getenv('IMAGES_DIR', default=os.path.join('media', 'images'))
    os.makedirs(IMAGES_DIR, exist_ok=True)

    on_reload()
    server = Server()
    server.watch('templates/template.html', on_reload)
    server.serve()


if __name__ == '__main__':
    main()



