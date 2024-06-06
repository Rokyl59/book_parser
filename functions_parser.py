import os
import requests
from requests.exceptions import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.history:
        raise HTTPError(f"Redirected to {response.url}")


def get_book_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
        return BeautifulSoup(response.text, 'html.parser')
    except (HTTPError, requests.RequestException):
        return None


def get_title_author(soup):
    title_tag = soup.find('h1')
    title_text = title_tag.text.strip()
    title_author = title_text.split('::')
    title, author = title_author
    return title.strip(), author.strip()


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Ссылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    safe_filename = sanitize_filename(filename) + '.txt'
    filepath = os.path.join(folder, safe_filename)

    os.makedirs(folder, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath
