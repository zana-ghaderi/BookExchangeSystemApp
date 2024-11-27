from typing import Optional

class Book:
    def __init__(self, book_id: Optional[int], title: str, author: str, isbn: str, edition: str, owner, condition: Optional[str] = None, genre: Optional[str] = None):
        self.book_id: Optional[int] = book_id
        self.title: str = title
        self.author: str = author
        self.isbn: str = isbn
        self.edition: str = edition
        self.owner = owner
        self.condition: Optional[str] = condition
        self.genre: Optional[str] = genre
        self.is_available: bool = True