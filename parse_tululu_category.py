import os
import requests
from bs4 import BeautifulSoup


base_url = 'http://tululu.org/l55/'


class TululuRedirectError(requests.HTTPError):
    pass


def check_for_redirect(response):
    if response.history and response.url == 'http://tululu.org/':
        raise TululuRedirectError(f"Redirected to main page: {response.url}")


def get_book_id(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'html.parser')
    book_cards = soup.find_all('div', class_='bookimage')

    book_ids = []
    for book_card in book_cards:
        book_link = book_card.find('a')['href']
        book_id = book_link.split('/b')[-1].split('/')[0]
        book_ids.append(int(book_id))

    return book_ids


def get_book_ids(start_page, end_page, dest_folder):
    if dest_folder:
        os.makedirs(dest_folder, exist_ok=True)

    all_book_ids = []
    for page in range(start_page, end_page + 1):
        url = f'{base_url}{page}/'
        try:
            book_ids = get_book_id(url)
            all_book_ids.extend(book_ids)
        except TululuRedirectError as e:
            print(f"Error: {e}")
            continue

    return all_book_ids, dest_folder
