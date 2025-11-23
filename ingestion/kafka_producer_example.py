"""
Example Kafka producer to simulate streaming ingestion.

This is a simple example using the `kafka-python` library to send
fake transaction messages into a Kafka topic.
"""

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

def create_sample_transaction():
    return {
        "txn_id": f"txn_{int(time.time() * 1000)}",
        "user": f"user_{random.randint(1, 1000)}",
        "txn_time": datetime.utcnow().isoformat(),
        "amt": round(random.uniform(10, 1000), 2),
        "curr": "USD",
        "cat": random.choice(["food", "travel", "shopping", "other"]),
        "country": random.choice(["US", "IN", "UK", "DE"])
    }

def main():
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    topic = "transactions_stream"

    try:
        while True:
            msg = create_sample_transaction()
            producer.send(topic, msg)
            print("Sent:", msg)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped producing.")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
