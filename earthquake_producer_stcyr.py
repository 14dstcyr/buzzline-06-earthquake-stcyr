import os, json, time
from dotenv import load_dotenv
from kafka import KafkaProducer
from datetime import datetime

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = os.getenv("EARTHQUAKE_TOPIC", "eq-topic")
print(f"Using topic from .env: {topic}")  # verification line

# Example streaming messages
earthquake_events = [
    {"id": 1, "magnitude": 6.2, "location": "California", "depth_km": 20},
    {"id": 2, "magnitude": 7.8, "location": "Chile", "depth_km": 40},
    {"id": 3, "magnitude": 4.9, "location": "Alaska", "depth_km": 15},
]

for event in earthquake_events:
    event["time"] = datetime.now(datetime.UTC).isoformat()
    producer.send(topic, event)
    print(f"Produced: {event}")
    time.sleep(2)


producer.flush()
