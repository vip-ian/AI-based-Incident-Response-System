from kafka import KafkaProducer, KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

class LogCollector:
    def __init__(self, kafka_server='localhost:9092', es_host='localhost', es_port=9200):
        self.kafka_server = kafka_server
        self.es = Elasticsearch([{'host': es_host, 'port': es_port}])

    def send_logs(self, logs_topic='logs_topic'):
        producer = KafkaProducer(
            bootstrap_servers=[self.kafka_server],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        sample_logs = [
            {"timestamp": "2023-10-15T10:00:00", "log_level": "INFO", "message": "System started successfully."},
            {"timestamp": "2023-10-15T10:01:00", "log_level": "ERROR", "message": "Failed to connect to database."},
            {"timestamp": "2023-10-15T10:02:00", "log_level": "WARNING", "message": "Disk usage is above 80%."}
        ]
        for log in sample_logs:
            producer.send(logs_topic, log)
            print(f"Sent log: {log}")
            time.sleep(1)

    def consume_and_store_logs(self, logs_topic='logs_topic'):
        consumer = KafkaConsumer(
            logs_topic,
            bootstrap_servers=[self.kafka_server],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='log-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        for message in consumer:
            log_data = message.value
            print(f"Received log: {log_data}")
            self.es.index(index='logs_index', body=log_data)