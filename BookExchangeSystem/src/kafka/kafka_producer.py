from confluent_kafka import Producer, KafkaError
from Intuit.BookExchangeSystem.src.config.config import kafka_producer_config
import json

class KafkaProducer:
    def __init__(self):
        self.producer = Producer(kafka_producer_config)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def send_message(self, topic, message):
        try:
            self.producer.produce(topic,
                                  json.dumps(message).encode('utf-8'),
                                  callback=self.delivery_report)
            self.producer.poll(0)
        except KafkaError as e:
            print(f'Error producing message: {e}')

    def flush(self):
        self.producer.flush()