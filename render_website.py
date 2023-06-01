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

    book_descriptions = []
    for filepath in glob.glob(os.path.join(json_dir, '*.json')):
        with open(filepath) as file:
            book_description = json.load(file)
        image_path = book_description['image'].split('/')
        image_dir = os.path.join('images', 'genre_55')
        image_file = os.path.join(image_dir, f'book_{image_path[-1]}')
        book_description['book_id'] = image_path[-1].split('.')[0]
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
