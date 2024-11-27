from confluent_kafka import Consumer, KafkaError, KafkaException
from Intuit.BookExchangeSystem.src.config.config import kafka_consumer_config
import json
import time

class KafkaConsumer:
    def __init__(self, topic, group_id):
        self.config = {
            **kafka_consumer_config,
            'group.id': group_id,
        }
        self.topic = topic
        self.consumer = None
        self.running = False

    def connect(self):
        if self.consumer is None:
            self.consumer = Consumer(self.config)
            self.consumer.subscribe([self.topic])

    def consume_messages(self, message_processor):
        self.running = True
        self.connect()
        try:
            while self.running:
                try:
                    msg = self.consumer.poll(1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            print(f'Reached end of partition: {msg.topic()} [{msg.partition()}]')
                        else:
                            print(f'Error while consuming message: {msg.error()}')
                    else:
                        try:
                            value = json.loads(msg.value().decode('utf-8'))
                            message_processor(value)
                        except json.JSONDecodeError as e:
                            print(f'Error decoding message: {e}')
                except KafkaException as e:
                    print(f"Kafka error: {e}")
                    time.sleep(5)  # Wait before attempting to reconnect
                    self.connect()  # Attempt to reconnect
        finally:
            self.consumer.close()

    def stop(self):
        self.running = False