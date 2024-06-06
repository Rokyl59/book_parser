# Загрузчик книг с Tululu

Этот скрипт позволяет загружать книги из онлайн-библиотеки Tululu.


## Основные возможности

* Проходит по страницам книг.

* Извлекает информацию о книгах, такую как название, автор, обложка, комментарии и жанры.

* Скачивает текст книги и обложку.

* Сохраняет полученные данные в файлах и выводит на экран во время работы скрипта.

* Пользователь может указать диапазон идентификаторов книг для загрузки через аргументы командной строки.

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Rokyl59/book_parser.git
```

2. Установите зависимости и python3:

```bash
pip install -r requirements.txt
```

## Использование

```bash
python main.py --start_id START_ID --end_id END_ID
```

* `--start_id`: Начальный идентификатор книги (по умолчанию 1).
* `--end_id`: Конечный идентификатор книги (по умолчанию 10).

Пример:

```bash
python main.py --start_id 20 --end_id 30
```

Эта команда загрузит книги с идентификаторами от 20 до 30.

