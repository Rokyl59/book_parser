import requests
from requests.exceptions import HTTPError
from functions_parser import download_txt, get_book_page, get_title_author, \
    get_image_url, download_image, get_comments, get_book_genre


def parse_book_page(page_soup, book_id):
    try:
        title, author = get_title_author(page_soup)
        image_url = get_image_url(page_soup, f'https://tululu.org/b{book_id}/')
        comments = get_comments(page_soup)
        genre = get_book_genre(page_soup)
        return {
            'title': title,
            'author': author,
            'image_url': image_url,
            'comments': comments,
            'genre': genre
        }
    except Exception as e:
        print(f"Error parsing book {book_id}: {e}")
        return None


def main(amount):
    for book_id in range(1, amount + 1):
        try:
            url = f'https://tululu.org/b{book_id}/'
            page_soup = get_book_page(url)
            if page_soup:
                book_data = parse_book_page(page_soup, book_id)
                if book_data:
                    txt_url = f'https://tululu.org/txt.php?id={book_id}'
                    filename = f"{book_id}. {book_data['title']}"
                    filepath = download_txt(txt_url, filename)
                    download_image(book_data['image_url'], f'{book_id}')
                    print(f'\nBook {book_id} downloaded: {filepath}')
                    print(f'Cover URL: {book_data["image_url"]}')
                    print(f'Genre: {book_data["genre"]}')
                    print("Comments:")
                    for comment in book_data["comments"]:
                        print(comment)
                else:
                    print(f'Book {book_id} data could not be parsed.\n')
            else:
                print(f'\nBook {book_id} not found on the site.')
        except HTTPError as e:
            print(f'\nBook {book_id} could not be downloaded: {e}')
        except requests.RequestException as e:
            print(f'An error occurred while downloading book {book_id}: {e}')


if __name__ == '__main__':
    main(10)
