import json
import os
import glob
from more_itertools import chunked, sliced
from livereload import Server

from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload():

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template(os.path.join('templates', 'template.html'))
    books_for_page = 10
    json_dir = os.path.join('comments', 'genre_55')
    os.makedirs('pages', exist_ok=True)
    file_name = os.path.join(json_dir, 'comments.json')
    with open(file_name, "r", encoding='utf-8') as file:
        file_data = file.read()
    book_comments = json.loads(file_data)

    image_dir = os.path.join('images', 'genre_55')
    book_descriptions = []
    for key, book_description in book_comments.items():
        image_path = book_description['image'].split('/')
        image_file = os.path.join(image_dir, f'book_{image_path[-1]}')
        book_description['image'] = image_file
        book_descriptions.append(book_description)

    pages = list(sliced(book_descriptions, books_for_page))
    pages_count = len(pages)
    for index, page_books in enumerate(pages):
        columns_books = list(chunked(page_books, 2))
        rendered_page = template.render(
            books=columns_books,
            max_page_num=pages_count,
            page_num=index+1,
            current_page_num=index+1,
        )
        with open(os.path.join('pages', f'index{index+1}.html'), 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():

    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename=os.path.join('pages', 'index1.html'))


if __name__ == '__main__':
    main()
