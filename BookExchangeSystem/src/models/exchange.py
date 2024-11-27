from datetime import datetime
from typing import Optional


class Exchange:
    def __init__(self, exchange_id, requester, provider, book_offered, book_requested, status="PENDING"):
        self.exchange_id = exchange_id
        self.requester = requester
        self.provider = provider
        self.book_offered = book_offered
        self.book_requested = book_requested
        self.status = status
        self.request_date = datetime.now()
        self.completion_date: Optional[datetime] = None

    def initiate_exchange(self):
        # Code to initiate exchange between two users
        pass

    def accept_exchange(self):
        # Code to accept an exchange
        self.status = "ACCEPTED"

    def reject_exchange(self):
        # Code to reject an exchange
        self.status = "REJECTED"

    def complete_exchange(self):
        # Code to mark exchange as completed
        self.status = "COMPLETED"

