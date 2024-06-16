import requests
from bs4 import BeautifulSoup
import argparse
import os


base_url = 'http://tululu.org/l55/'


def get_all_books_ids(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    book_cards = soup.find_all('div', class_='bookimage')

    book_ids = []
    for book_card in book_cards:
        book_link = book_card.find('a')['href']
        book_id = book_link.split('/b')[-1].split('/')[0]
        book_ids.append(int(book_id))

    return book_ids


def main():
    parser = argparse.ArgumentParser(description='Download books from tululu.org')
    parser.add_argument('--start_page', type=int, help='Start page number', default=1)
    parser.add_argument('--end_page', type=int, help='End page number', default=1)
    parser.add_argument('--dest_folder', type=str, help='Destination folder path', default='')
    parser.add_argument('--skip_imgs', action='store_true', help='Skip downloading images')
    parser.add_argument('--skip_txt', action='store_true', help='Skip downloading text files')
    args = parser.parse_args()

    start_page = args.start_page
    end_page = args.end_page
    dest_folder = args.dest_folder
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt

    if dest_folder:
        os.makedirs(dest_folder, exist_ok=True)

    all_book_ids = []
    for page in range(start_page, end_page + 1):
        url = f'{base_url}{page}/'
        book_ids = get_all_books_ids(url)
        all_book_ids.extend(book_ids)

    return all_book_ids, dest_folder, skip_imgs, skip_txt


if __name__ == '__main__':
    book_ids, dest_folder, skip_imgs, skip_txt = main()
    print(f'IDs книг: {book_ids}')
