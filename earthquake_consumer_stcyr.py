import os
import json
from dotenv import load_dotenv
from kafka import KafkaConsumer
import matplotlib.pyplot as plt
from collections import deque, Counter

# ---------------------------
# Load environment
# ---------------------------
load_dotenv()
topic = os.getenv("EARTHQUAKE_TOPIC", "eq-topic")

# ---------------------------
# Kafka Consumer
# ---------------------------
consumer = KafkaConsumer(
    topic,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

# ---------------------------
# Visualization Setup
# ---------------------------
plt.ion()  # interactive mode

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# Line chart (magnitudes over time)
magnitudes = deque(maxlen=20)   # last 20 events
locations = deque(maxlen=20)
line, = ax1.plot([], [], marker="o", linestyle="--")
ax1.set_ylabel("Magnitude")
ax1.set_title("Live Earthquake Magnitudes")

# Bar chart (counts per location)
quake_counts = Counter()

# ---------------------------
# Stream and Plot
# ---------------------------
print("Consumer with dual visualization listening...")

for i, message in enumerate(consumer, start=1):
    quake = message.value
    print(f"Consumed: {quake}")

    # Update line chart
    magnitudes.append(quake["magnitude"])
    locations.append(quake["location"])

    line.set_xdata(range(len(magnitudes)))
    line.set_ydata(magnitudes)
    ax1.set_xticks(range(len(magnitudes)))
    ax1.set_xticklabels(locations, rotation=45, ha="right")
    ax1.relim()
    ax1.autoscale_view()

    # Update bar chart
    quake_counts[quake["location"]] += 1
    ax2.clear()
    ax2.bar(quake_counts.keys(), quake_counts.values())
    ax2.set_ylabel("Count")
    ax2.set_title("Earthquake Counts by Location")

    # Redraw both
    plt.tight_layout()
    plt.draw()
    plt.pause(0.5)
