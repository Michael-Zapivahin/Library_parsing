# Book parser tutulu.org

Program downloads books from https://tululu.org/

## How to install

Python3 should already be installed. 
Use pip or pip3, if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
```

## Program uses an environment variable

#### Variables:

`BOOKS_DIR` directory for saving your books, `default='books'`

`IMAGES_DIR` directory for saving your pictures, `default='images'`

### How to start

```
python main.py --start_page 0 --end_page 2
```

'--start_page' page's number starting from which the script will begin to fetch the books.

'--end_page' page's number for ending.

'--skip_imgs' argument turn off book covers download if 'True' is specified

'--skip_txt' argument turn off book texts download if 'True' is specified

'--dest_folder' argument changes the books download destination folder

'--json_path' argument changes the JSON file destination folder

## The aim of the project 
The code is written for educational purposes on the online course for web developers [Devman практика Python](https://dvmn.org/)

