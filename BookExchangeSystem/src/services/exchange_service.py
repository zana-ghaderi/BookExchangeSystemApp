import uuid
from datetime import datetime

class ExchangeService:
    def __init__(self):
        self.exchanges = {}

    def request_exchange(self, exchange):
        exchange.exchange_id = str(uuid.uuid4())  # Generate a unique ID
        self.exchanges[exchange.exchange_id] = exchange
        return exchange

    def get_exchange_by_id(self, exchange_id):
        return self.exchanges.get(exchange_id)

    def update_exchange_status(self, exchange_id, status):
        exchange = self.get_exchange_by_id(exchange_id)
        if exchange:
            exchange.status = status
            if status == "COMPLETED":
                exchange.completion_date = datetime.now()
            return exchange
        raise ValueError("Exchange not found")

    def get_user_exchanges(self, user_id):
        return [exchange for exchange in self.exchanges.values() if exchange.requester.user_id == user_id]