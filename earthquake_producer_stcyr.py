import os, json, time
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = os.getenv("EARTHQUAKE_TOPIC", "eq-topic")

# Example streaming messages
earthquake_events = [
    {"id": 1, "magnitude": 5.2, "location": "California", "depth_km": 10},
    {"id": 2, "magnitude": 6.8, "location": "Chile", "depth_km": 33},
    {"id": 3, "magnitude": 4.9, "location": "Alaska", "depth_km": 15},
]

for event in earthquake_events:
    producer.send(topic, event)
    print(f"Produced: {event}")
    time.sleep(2)

producer.flush()
