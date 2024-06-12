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
    title_tag = soup.find('h1')
    title_text = title_tag.text.strip()
    title_author = title_text.split('::')
    title, author = title_author
    return title.strip(), author.strip()


def get_image_url(soup, base_url):
    image_tag = soup.find('div', class_='bookimage').find('img')
    image_src = image_tag['src']
    return urljoin(base_url, image_src)


def get_comments(soup):
    comments_divs = soup.find_all('div', class_='texts')
    comments = []
    for div in comments_divs:
        comment_tag = div.find('span', class_='black')
        comment_text = comment_tag.get_text(strip=True)
        comments.append(comment_text.strip())
    return comments


def get_book_genres(soup):
    genre_tags = soup.find('span', class_='d_book').find_all('a')
    genres = [tag.text.strip() for tag in genre_tags]
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
