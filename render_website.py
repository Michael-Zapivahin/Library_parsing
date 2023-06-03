import json
import os
from more_itertools import chunked, sliced
from livereload import Server
from dotenv import load_dotenv

from jinja2 import Environment, FileSystemLoader, select_autoescape

server = Server()


def on_reload():
    load_dotenv()
    descriptions_dir = os.getenv('COMMENTS_DIR', default='descriptions')
    os.makedirs(descriptions_dir, exist_ok=True)
    images_dir = os.getenv('IMAGES_DIR', default='descriptions')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs('pages', exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template(os.path.join('templates', 'template.html'))
    books_for_page = 10
    columns_count = 2

    descriptions_dir = os.path.join(descriptions_dir, 'genre_55')
    file_name = os.path.join(descriptions_dir, 'descriptions.json')
    with open(file_name, 'r', encoding='utf-8') as file:
        book_comments = json.load(file)

    image_dir = os.path.join(images_dir, 'genre_55')
    book_descriptions = []
    for key, book_description in book_comments.items():
        image_path = book_description['image'].split('/')
        image_file = os.path.join(image_dir, f'book_{image_path[-1]}')
        book_description['image'] = image_file
        book_descriptions.append(book_description)
        book_description['book_id'] = key
        book_description['genre'] = '55'

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

    on_reload()

    # server = Server()
    # server.watch('template.html', on_reload)
    # server.serve(root='.', default_filename=os.path.join('pages', 'index1.html'))


if __name__ == '__main__':
    main()


server.watch('templates/template.html', on_reload)
server.serve()
