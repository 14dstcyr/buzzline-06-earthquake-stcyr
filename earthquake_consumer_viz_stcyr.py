import matplotlib
matplotlib.use("TkAgg")   

import os
import json
from dotenv import load_dotenv
from kafka import KafkaConsumer
import matplotlib.pyplot as plt
from collections import deque, defaultdict

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
plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Deques for time-series data
magnitudes = deque(maxlen=20)
locations = deque(maxlen=20)

# Dictionary for counts
quake_counts = defaultdict(int)

# Line plot (ax1)
line, = ax1.plot([], [], marker="o", linestyle="--")
ax1.set_xlabel("Event #")
ax1.set_ylabel("Magnitude")
ax1.set_title("Live Earthquake Magnitudes")

# Bar plot (ax2)
bars = None
ax2.set_title("Earthquake Counts by Location")
ax2.set_ylabel("Count")

# ---------------------------
# Stream and Plot
# ---------------------------
print("Consumer with visualization listening...")

for i, message in enumerate(consumer, start=1):
    quake = message.value
    print(f"Consumed: {quake}")

    # Update data
    magnitudes.append(quake["magnitude"])
    locations.append(quake["location"])
    quake_counts[quake["location"]] += 1

    # Update line plot
    line.set_xdata(range(len(magnitudes)))
    line.set_ydata(magnitudes)
    ax1.set_xticks(range(len(magnitudes)))
    ax1.set_xticklabels(locations, rotation=45, ha="right")
    ax1.relim()
    ax1.autoscale_view()

    # Update bar plot
    ax2.clear()
    ax2.bar(quake_counts.keys(), quake_counts.values(), color="skyblue")
    ax2.set_title("Earthquake Counts by Location")
    ax2.set_ylabel("Count")

    # Redraw
    plt.tight_layout()
    plt.draw()
    plt.pause(0.5)
