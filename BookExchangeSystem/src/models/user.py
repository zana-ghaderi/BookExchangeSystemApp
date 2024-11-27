from typing import List, Optional

class User:
    def __init__(self, user_id: Optional[int], name: str, email: str, password_hash: str):
        self.user_id: Optional[int] = user_id
        self.name: str = name
        self.email: str = email
        self.password_hash: str = password_hash
        self.owned_books: List = []
        self.exchanges: List = []
        self.rating: float = 0.0