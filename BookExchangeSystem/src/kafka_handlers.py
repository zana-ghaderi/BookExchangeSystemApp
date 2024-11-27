import json

from Intuit.BookExchangeSystem.src.kafka.kafka_consumer import KafkaConsumer
from Intuit.BookExchangeSystem.src.services.book_service import BookService
from Intuit.BookExchangeSystem.src.services.notification_service import NotificationService
from Intuit.BookExchangeSystem.src.services.user_service import UserService


class KafkaMessageHandler:
    def __init__(self):
        self.book_service = BookService(UserService())
        self.notification_service = NotificationService()
        self.consumer = KafkaConsumer('book_topic', 'book_group')

    def handle_message(self, message):
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                print(f"Invalid JSON message: {message}")
                return

        action = message.get('action')
        if action == 'add_book':
            self.handle_add_book(message)
        elif action == 'update_book':
            self.handle_update_book(message)
        elif action == 'delete_book':
            self.handle_delete_book(message)
        else:
            print(f"Unknown action: {action}")

    def handle_add_book(self, message):
        book_id = message.get('book_id')
        title = message.get('title')
        author = message.get('author')
        print(f"Book added/updated: {title} by {author} (ID: {book_id})")

    def handle_update_book(self, message):
        book_id = message.get('book_id')
        title = message.get('title')
        author = message.get('author')
        print(f"Book updated: {title} by {author} (ID: {book_id})")


    def handle_add_book(self, message):
        book_id = message.get('book_id')
        title = message.get('title')
        author = message.get('author')
        print(f"New book added: {title} by {author} (ID: {book_id})")
        # You could send a notification to interested users here
        # self.notification_service.send_notification(...)

    def handle_update_book(self, message):
        book_id = message.get('book_id')
        title = message.get('title')
        author = message.get('author')
        print(f"Book updated: {title} by {author} (ID: {book_id})")
        # You could update caches or send notifications here

    def handle_delete_book(self, message):
        book_id = message.get('book_id')
        print(f"Book deleted: ID {book_id}")
        # You could update caches or send notifications here

    def start_consuming(self):
        print("Starting to consume messages...")
        self.consumer.consume_messages(self.handle_message)

    def stop_consuming(self):
        self.consumer.stop()

if __name__ == "__main__":
    handler = KafkaMessageHandler()
    try:
        handler.start_consuming()
    except KeyboardInterrupt:
        print("Stopping consumer...")
        handler.stop_consuming()