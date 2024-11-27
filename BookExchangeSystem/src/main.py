import time
import threading
from Intuit.BookExchangeSystem.src.services.book_service import BookService
from Intuit.BookExchangeSystem.src.services.user_service import UserService
from Intuit.BookExchangeSystem.src.services.exchange_service import ExchangeService
from Intuit.BookExchangeSystem.src.kafka_handlers import KafkaMessageHandler
from Intuit.BookExchangeSystem.src.models.user import User
from Intuit.BookExchangeSystem.src.models.book import Book
from Intuit.BookExchangeSystem.src.models.exchange import Exchange


def start_kafka_consumer():
    while True:
        try:
            handler = KafkaMessageHandler()
            handler.start_consuming()
        except Exception as e:
            print(f"Error in Kafka consumer: {e}")
            print("Attempting to restart Kafka consumer in 5 seconds...")
            time.sleep(5)


def test_user_registration(user_service):
    print("\n--- Testing User Registration ---")
    users_to_register = [
        User(None, "Alice Smith", "alice@example.com", "password123"),
        User(None, "Bob Johnson", "bob@example.com", "password456"),
        User(None, "Charlie Brown", "charlie@example.com", "password789")
    ]

    for user in users_to_register:
        try:
            registered_user = user_service.register_user(user)
            print(f"Registered User: {registered_user.name} (ID: {registered_user.user_id})")
        except ValueError as e:
            print(f"Failed to register user {user.name}: {str(e)}")

    return user_service.get_user_by_email("alice@example.com"), user_service.get_user_by_email("bob@example.com")


def test_book_management(book_service, user):
    print("\n--- Testing Book Management ---")
    books_to_add = [
        Book(None, "The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "First Edition", user, "Good",
             "Fiction"),
        Book(None, "To Kill a Mockingbird", "Harper Lee", "9780446310789", "Reprint", user, "Excellent", "Fiction"),
        Book(None, "1984", "George Orwell", "9780451524935", "Reprint", user, "Good", "Fiction")
    ]

    added_books = []
    for book in books_to_add:
        added_book = book_service.add_book(book)
        print(f"Added/Updated Book: {added_book.title} (ID: {added_book.book_id})")
        added_books.append(added_book)

    # Update a book
    added_books[0].condition = "Excellent"
    updated_book = book_service.update_book(added_books[0])
    print(f"Updated Book: {updated_book.title} (New Condition: {updated_book.condition})")

    # Get all available books
    available_books = book_service.get_available_books()
    print(f"Available Books: {[book.title for book in available_books]}")

    return added_books[0], added_books[1]


def test_exchange(exchange_service, book1, user1, book2, user2):
    print("\n--- Testing Book Exchange ---")
    if book1 is None or book2 is None:
        print("Cannot test exchange: Books are not available")
        return None

    exchange = Exchange(None, user1, user2, book1, book2)
    try:
        created_exchange = exchange_service.request_exchange(exchange)
        print(f"Created Exchange: ID {created_exchange.exchange_id}")

        # Accept the exchange
        updated_exchange = exchange_service.update_exchange_status(created_exchange.exchange_id, "ACCEPTED")
        print(f"Updated Exchange Status: {updated_exchange.status}")

        return created_exchange
    except Exception as e:
        print(f"Failed to create or update exchange: {str(e)}")
        return None


def main():
    # Initialize services
    user_service = UserService()
    book_service = BookService(user_service)
    exchange_service = ExchangeService()

    # Start Kafka consumer in a separate thread
    kafka_thread = threading.Thread(target=start_kafka_consumer)
    kafka_thread.daemon = True  # Set as daemon thread
    kafka_thread.start()

    try:
        # Test user registration
        user1, user2 = test_user_registration(user_service)

        # Test book management
        book1, book2 = test_book_management(book_service, user1)

        # Test book exchange
        exchange = test_exchange(exchange_service, book1, user1, book2, user2)

        # Keep the main thread running for a while to allow Kafka messages to be processed
        print("\nWaiting for Kafka messages to be processed...")
        time.sleep(10)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Shutting down...")
        # Stop the Kafka consumer
        kafka_thread.join(timeout=5)


if __name__ == "__main__":
    main()