import argparse
import json
import os
import math
import pickle

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


BOOKS_PER_PAGE = 10
BOOK_COLUMNS = 2


def on_reload():
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-j', '--json_path', help='Путь к json файлу с результатами',
    #     default='comments'
    # )
    # args = parser.parse_args()
    # json_path = args.json_path

    json_path = 'comments/genre_55/book_59678.json'

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('templates/template.html')
    books_for_page = 10
    pages_count = 1
    page_id = 1
    with open(f'{json_path}', 'r') as file:
        book_descriptions = json.load(file)
    # book_descriptions_per_page = list(chunked(book_descriptions, BOOKS_PER_PAGE))
    # pages_count = math.ceil(len(book_descriptions)/BOOKS_PER_PAGE)
    # for index, books in enumerate(book_descriptions_per_page, start=1):
    #     books_for_page = list(chunked((books), BOOK_COLUMNS))
    rendered_page = template.render(
        book_descriptions=book_descriptions,
        pages_count=pages_count,
        number_page=page_id
    )
    os.makedirs('pages', exist_ok=True)
    with open(f'pages/index{page_id}.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index1.html')


if __name__ == '__main__':
    main()
