import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from os import sep


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template/template.html')
    books = []
    books.append(
        {
            'title': '1-tree-1',
            'autor': 'William',
            'image': 'images/book5.jpg'
        }
    )
    books.append(
        {
            'title': '1-tree-2',
            'autor': 'William',
            'image': 'images/book5.jpg'
        }
    )
    # books = json.dumps(books)
    print(books)
    rendered_page = template.render(books=books, sep=sep)
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    main()
