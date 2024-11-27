kafka_producer_config = {
    'bootstrap.servers': 'localhost:9092'
}

kafka_consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'book_exchange_group',
    'auto.offset.reset': 'earliest',
    'session.timeout.ms': 6000,
    'heartbeat.interval.ms': 3000
}

DB_CONFIG = {
    'database': 'exchange_db',
    'user': 'zana',
    'password': 'test123',
    'host': 'localhost',
    'port': '5432'
}