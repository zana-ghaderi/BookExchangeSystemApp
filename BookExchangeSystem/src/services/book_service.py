import json

import psycopg2
from Intuit.BookExchangeSystem.src.config.config import DB_CONFIG
import Intuit.BookExchangeSystem.src.database.database as db_util
from Intuit.BookExchangeSystem.src.kafka.kafka_producer import KafkaProducer
from Intuit.BookExchangeSystem.src.models.book import Book


class BookService:
    def __init__(self, user_service):
        self.connection = psycopg2.connect(**DB_CONFIG)
        self.kafka_producer = KafkaProducer()
        self.user_service = user_service

    def add_book(self, book):
        # Check if the book already exists
        existing_book = self.get_book_by_isbn(book.isbn)
        if existing_book:
            print(f"Book with ISBN {book.isbn} already exists. Updating instead of adding.")
            return self.update_book(existing_book)

        columns = ['title', 'author', 'isbn', 'edition', 'condition', 'genre', 'owner_id', 'is_available']
        values = [book.title, book.author, book.isbn, book.edition, book.condition, book.genre,
                  book.owner.user_id, book.is_available]
        book.book_id = db_util.insert_record('books', columns, values, self.connection)

        # Send Kafka message
        message = json.dumps({
            'action': 'add_book',
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author
        })
        self.kafka_producer.send_message('book_topic', message)
        return book

        # self.books[book.book_id] = book
        # return book

    def get_book_by_isbn(self, isbn):
        columns = ['id', 'title', 'author', 'isbn', 'edition', 'condition', 'genre', 'owner_id', 'is_available']
        condition = 'WHERE isbn = %s'
        books_data = db_util.get_records('books', columns, self.connection, condition, (isbn,))
        if books_data:
            book_data = books_data[0]
            return Book(book_data[0], book_data[1], book_data[2], book_data[3], book_data[4],
                        self.user_service.get_user_by_id(book_data[7]), book_data[5], book_data[6])
        return None

    def get_book_by_id(self, book_id):
        columns = ['id', 'title', 'author', 'isbn', 'edition', 'condition', 'genre', 'owner_id', 'is_available']
        book_data = db_util.get_record_by_id('books', columns, book_id, self.connection)
        if book_data:
            return Book(*book_data)
        return None

        #return self.books.get(book_id, None)

    def update_book(self, book):
        columns = ['title', 'author', 'isbn', 'edition', 'condition', 'genre', 'owner_id', 'is_available']
        values = [book.title, book.author, book.isbn, book.edition, book.condition, book.genre, book.owner.user_id,
                  book.is_available]
        db_util.update_record('books', columns, values, book.book_id, self.connection)

        # Send Kafka message
        message = json.dumps({
            'action': 'update_book',
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author
        })
        self.kafka_producer.send_message('book_topic', message)
        return book

        # if book.id not in self.books:
        #     raise ValueError("Book not found")
        # self.books[book.id] = book
        # return book

    def delete_book(self, book_id):
        db_util.delete_record('books', book_id, self.connection)

        # Send Kafka message
        message = {
            'action': 'delete_book',
            'book_id': book_id
        }
        self.kafka_producer.send_message('book_topic', message)

        #self.books.pop(book_id, None)

    def get_available_books(self):
        columns = ['id', 'title', 'author', 'isbn', 'edition', 'condition', 'genre', 'owner_id', 'is_available']
        condition = 'WHERE is_available = TRUE'
        books_data = db_util.get_records('books', columns, self.connection, condition)
        unique_books = {}
        for book_data in books_data:
            isbn = book_data[3]
            if isbn not in unique_books:
                unique_books[isbn] = Book(book_data[0], book_data[1], book_data[2], book_data[3], book_data[4],
                                          self.user_service.get_user_by_id(book_data[7]), book_data[5], book_data[6])
        return list(unique_books.values())

        #return [book for book in self.books.values() if book.is_available]

    def __del__(self):
        self.kafka_producer.flush()
