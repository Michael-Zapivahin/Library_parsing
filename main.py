
import os
import requests

from dotenv import load_dotenv


def main():
    load_dotenv()
    os.getenv('DEBUG')
    media_dir = os.getenv('MEDIA_DIR')
    os.makedirs(media_dir, exist_ok=True)
    # https: // tululu.org / txt.php?id = 32168
    for book_id in range(68, 78, 1):
        book_url = f'https://tululu.org/txt.php?id=321{book_id}'
        path = os.path.join(media_dir, f'id_321{book_id}')
        file_name = f'{path}.txt'
        response = requests.get(book_url)
        response.raise_for_status()
        book = response.text
        print(book)
        with open(file_name, 'w') as file:
            file.write(book)



if __name__ == '__main__':
    main()


