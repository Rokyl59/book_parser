import os
import requests


def main(amount):
    os.makedirs('books', exist_ok=True)
    for book_id in range(1, amount + 1):
        url = f'https://tululu.org/txt.php?id={book_id}'
        response = requests.get(url)
        response.raise_for_status()
        with open(f'books/book{book_id}.txt', 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    main(10)
