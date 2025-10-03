import os, json
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()

topic = os.getenv("EARTHQUAKE_TOPIC", "eq-topic")

consumer = KafkaConsumer(
    topic,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

print("Consumer listening...")

for message in consumer:
    print(f"Consumed: {message.value}")
