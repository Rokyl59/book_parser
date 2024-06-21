import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, RequestException


base_url = 'http://tululu.org/l55/'


class TululuRedirectError(requests.HTTPError):
    pass


def check_for_redirect(response):
    if response.history:
        raise TululuRedirectError(f"Redirected to main page: {response.url}")


def get_book_ids_from_page(url):
    try:
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
    except (HTTPError, RequestException) as error:
        print(f'An error occurred while downloading book {book_id}: {error}')

    except ConnectionError as error:
        print(f'Connection error occurred while downloading book {book_id}: {error}')
        print('Retrying in 5 seconds...')
        time.sleep(5)


def get_book_ids(start_page, end_page):
    all_book_ids = []
    for page in range(start_page, end_page + 1):
        url = f'{base_url}{page}/'
        try:
            book_ids = get_book_ids_from_page(url)
            all_book_ids.extend(book_ids)
        except TululuRedirectError as e:
            print(f"Error: {e}")
            continue

    return all_book_ids
