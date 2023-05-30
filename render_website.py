import json
import os
import glob
from more_itertools import chunked, sliced
from http.server import HTTPServer, SimpleHTTPRequestHandler
import livereload

from jinja2 import Environment, FileSystemLoader, select_autoescape
from os import sep


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-j', '--json_path', help='Путь к json файлу с результатами',
    #     default='comments'
    # )
    # args = parser.parse_args()
    # json_path = args.json_path

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('templates/template.html')
    books_for_page = 10
    pages_count = 1
    page_id = 1
    json_dir = 'comments/genre_55/'
    os.makedirs('pages', exist_ok=True)

    book_descriptions = []
    for filepath in glob.glob(os.path.join(json_dir, '*.json')):
        with open(filepath) as file:
            book_description = json.load(file)
        image_path = book_description['image'].split('/')
        image_file = f'images/genre_55/book_{image_path[-1]}'
        book_description['book_id'] = image_path[-1].split('.')[0]
        book_description['image'] = image_file
        book_descriptions.append(book_description)

    pages = list(sliced(book_descriptions, books_for_page))
    pages_count = len(pages)
    for index, page_books in enumerate(pages):
        columns_books = list(chunked(page_books, 2))
        rendered_page = template.render(
            books=columns_books,
            pages_count=pages_count,
            number_page=index+1,
            current_page=index+1,
        )
        with open(f'pages/index{index+1}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


if __name__ == '__main__':
    main()
