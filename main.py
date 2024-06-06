import requests
from requests.exceptions import HTTPError
from functions_parser import download_txt, get_book_page, get_title_author, \
    get_image_url, download_image, get_comments


def main(amount):
    for book_id in range(1, amount + 1):
        try:
            url = f'https://tululu.org/b{book_id}/'
            page_soup = get_book_page(url)
            if page_soup:
                title, author = get_title_author(page_soup)
                image_url = get_image_url(page_soup, url)
                txt_url = f'https://tululu.org/txt.php?id={book_id}'
                filename = f"{book_id}. {title} - {author}"
                filepath = download_txt(txt_url, filename)
                download_image(image_url, f'{book_id}')
                print(f'Book {book_id} downloaded successfully: {filepath}')
                print(f'Cover URL: {image_url}')
                comments = get_comments(page_soup)
                print("Comments:")
                for comment in comments:
                    print(comment)
            else:
                print(f'Book {book_id} not found on the site.')
        except HTTPError as e:
            print(f'Book {book_id} could not be downloaded: {e}')
        except requests.RequestException as e:
            print(f'An error occurred while downloading book {book_id}: {e}')


if __name__ == '__main__':
    main(10)
