class SearchService:
    def __init__(self, book_service, user_service):
        self.book_service = book_service
        self.user_service = user_service

    def search_books(self, query):
        return [self.book_service.books[book_id] for book_id in self.book_service.books if query.lower() in self.book_service.books[book_id].title.lower() or query.lower() in self.book_service.books[book_id].author.lower()]

    def search_users(self, query):
        return [self.user_service.users[user_id] for user_id in self.user_service.users if query.lower() in self.user_service.users[user_id].username.lower() or query.lower() in self.user_service.users[user_id].email.lower()]
