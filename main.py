import time
import json
from requests.exceptions import HTTPError, RequestException
from functions_parser import download_txt, get_book_page, get_title_author, \
    get_image_url, download_image, get_comments, get_book_genres
from parse_tululu_category import main as get_book_ids
import argparse
import os


def parse_book_page(page_soup, book_url):
    title, author = get_title_author(page_soup)
    image_url = get_image_url(page_soup, book_url)
    comments = get_comments(page_soup)
    genres = get_book_genres(page_soup)
    return {
        'title': title,
        'author': author,
        'image_url': image_url,
        'comments': comments,
        'genres': genres
    }


def main():
    parser = argparse.ArgumentParser(description='Download books from tululu.org')
    parser.add_argument('--start_page', type=int, help='Start page number', default=1)
    parser.add_argument('--end_page', type=int, help='End page number', default=5)
    parser.add_argument('--dest_folder', type=str, help='Destination folder path', default='')
    parser.add_argument('--skip_imgs', action='store_true', help='Skip downloading images')
    parser.add_argument('--skip_txt', action='store_true', help='Skip downloading text files')
    args = parser.parse_args()

    book_ids, dest_folder, skip_imgs, skip_txt = get_book_ids()

    books_data = []
    for book_id in book_ids:
        while True:
            try:
                book_url = f'https://tululu.org/b{book_id}/'
                book_page_soup = get_book_page(book_url)
                book_page = parse_book_page(book_page_soup, book_url)

                if not skip_txt:
                    base_url = 'https://tululu.org/txt.php'
                    params = {'id': book_id}
                    txt_filename = f"{book_id}. {book_page['title']}"
                    txt_filepath = download_txt(base_url, params, txt_filename, folder=os.path.join(dest_folder, 'books'))
                    book_page['txt_filepath'] = txt_filepath

                if not skip_imgs:
                    image_folder = os.path.join(dest_folder, 'images')
                    download_image(book_page['image_url'], f'{book_id}', folder=image_folder)

                books_data.append(book_page)

                print(f'\nBook {book_id} downloaded:')
                if not skip_txt:
                    print(f'Text saved: {txt_filepath}')
                if not skip_imgs:
                    print(f'Cover URL: {book_page["image_url"]}')
                print(f'Genres: {book_page["genres"]}')
                print("Comments:")
                for comment in book_page["comments"]:
                    print(comment)

                print(f'Ссылка на книгу: {book_url}')

                break

            except (HTTPError, RequestException) as error:
                print(f'An error occurred while downloading book {book_id}: {error}')
                break

            except ConnectionError as error:
                print(f'Connection error occurred while downloading book {book_id}: {error}')
                print('Retrying in 5 seconds...')
                time.sleep(5)

    if dest_folder:
        json_filepath = os.path.join(dest_folder, 'books_data.json')
        with open(json_filepath, 'w', encoding='utf-8') as json_file:
            json.dump(books_data, json_file, ensure_ascii=False, indent=4)
            print(f'JSON file saved: {json_filepath}')


if __name__ == '__main__':
    main()
