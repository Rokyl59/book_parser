import requests
from bs4 import BeautifulSoup


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
    all_book_ids = []
    for page in range(1, 5):
        url = f'{base_url}{page}/'
        book_ids = get_all_books_ids(url)
        all_book_ids.extend(book_ids)

    return all_book_ids


if __name__ == '__main__':
    book_ids = main()
    print(f'IDs книг: {book_ids}')
