import time
import json
from requests.exceptions import HTTPError, RequestException
from functions_parser import download_txt, get_book_page, get_title_author, \
    get_image_url, download_image, get_comments, get_book_genres
from parse_tululu_category import main as get_book_ids


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
    book_ids = get_book_ids()

    books_pages = []
    for book_id in book_ids:
        while True:
            try:
                book_url = f'https://tululu.org/b{book_id}/'
                book_page_soup = get_book_page(book_url)
                book_page = parse_book_page(book_page_soup, book_url)

                base_url = 'https://tululu.org/txt.php'
                params = {'id': book_id}
                txt_filename = f"{book_id}. {book_page['title']}"
                txt_filepath = download_txt(base_url, params, txt_filename)
                download_image(book_page['image_url'], f'{book_id}')

                book_page['txt_filepath'] = txt_filepath
                books_pages.append(book_page)

                print(f'\nBook {book_id} downloaded: {txt_filepath}')
                print(f'Cover URL: {book_page["image_url"]}')
                print(f'Genres: {book_page["genres"]}')
                print("Comments:")
                for comment in book_page["comments"]:
                    print(comment)

                break

            except (HTTPError, RequestException) as error:
                print(f'An error occurred while downloading book {book_id}: {error}')
                break

            except ConnectionError as error:
                print(f'Connection error occurred while downloading book {book_id}: {error}')
                print('Retrying in 5 seconds...')
                time.sleep(5)

    with open('books_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_pages, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
