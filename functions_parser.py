import os
import requests
from requests.exceptions import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote


def check_for_redirect(response):
    if response.history:
        raise HTTPError(f"Redirected to {response.url}")


def get_book_page(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'html.parser')


def get_title_author(soup):
    title_text = soup.select_one('h1').get_text(strip=True)
    title, author = map(str.strip, title_text.split('::'))
    return title, author


def get_image_url(soup, base_url):
    image_src = soup.select_one('div.bookimage img')['src']
    return urljoin(base_url, image_src)


def get_comments(soup):
    comments = [tag.get_text(strip=True) for tag in soup.select('div.texts span.black')]
    return comments


def get_book_genres(soup):
    genres = [tag.get_text(strip=True) for tag in soup.select('span.d_book a')]
    return genres if genres else None


def download_txt(url, params, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Ссылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    safe_filename = f"{sanitize_filename(filename)}.txt"
    filepath = os.path.join(folder, safe_filename)
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def download_image(url, filename, folder='images/'):
    """Функция для скачивания изображений.
    Args:
        url (str): Ссылка на изображение, которое нужно скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до скачанного изображения.
    """
    parsed_url = urlparse(url)
    filename, file_extension = os.path.splitext(parsed_url.path)
    decoded_filename = unquote(os.path.basename(filename))
    safe_filename = sanitize_filename(decoded_filename)
    filename_with_extension = f"{safe_filename}{file_extension}"
    filepath = os.path.join(folder, filename_with_extension)
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath
