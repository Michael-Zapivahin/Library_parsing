import requests
from bs4 import BeautifulSoup


def beautiful_soup(url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup.find('h1', class_="entry-title").text, '\n')
    print(soup.find('img', class_='attachment-post-image')['src'], '\n')
    print(soup.find(class_="entry-content").text)


def main():
    beautiful_soup()


if __name__ == '__main__':
    main()
