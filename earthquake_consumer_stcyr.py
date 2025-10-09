import os, json
from dotenv import load_dotenv
from kafka import KafkaConsumer
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random  # only if you simulate data

# --- Load environment variables ---
load_dotenv()
topic = os.getenv("EARTHQUAKE_TOPIC", "eq-topic")

# --- Connect to Kafka topic ---
consumer = KafkaConsumer(
    topic,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

print("Consumer listening...")

# --- Visualization setup ---
WINDOW_MINUTES = 5
recent_events = []

# create /images folder if it doesn't exist
os.makedirs("images", exist_ok=True)
last_save_time = datetime.now()  # track time for periodic snapshots
SAVE_INTERVAL = 60  # seconds between saving images

def compute_counts(events):
    """Aggregate event counts per minute"""
    times = [t.replace(second=0, microsecond=0) for t, *_ in events]
    buckets = {}
    for t in times:
        buckets[t] = buckets.get(t, 0) + 1
    xs = sorted(buckets.keys())
    ys = [buckets[t] for t in xs]
    return xs, ys

# --- Matplotlib setup ---
plt.ion()
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.4)  # adds spacing between plots

# --- Dashboard style customization ---
for ax in (ax1, ax2, ax3):
    ax.set_facecolor("#B8BBAB57")  # soft sage-gray background
    ax.tick_params(colors="blue")    # blue tick marks and labels
    ax.title.set_color("blue")       # blue titles
    ax.xaxis.label.set_color("blue") # blue x-axis label
    ax.yaxis.label.set_color("blue") # blue y-axis label
    ax.grid(True, color="gray", linestyle="--", alpha=0.4)  # subtle gridlines

# --- Main loop ---
for message in consumer:
    try:
        event = message.value

        # Use simulated fields if missing
        # Prefer real timestamp from producer, else fallback
        if "time" in event:
            event_time = datetime.fromisoformat(event["time"])
        else:
            event_time = datetime.now()
        
        # Simulate events spaced out by 1 minute for testing
        magnitude = event.get("magnitude", random.uniform(2.5, 6.5))
        lat = event.get("latitude", random.uniform(-90, 90))
        lon = event.get("longitude", random.uniform(-180, 180))

        # Store in sliding window
        recent_events.append((event_time, magnitude, lat, lon))
        cutoff = datetime.now() - timedelta(minutes=WINDOW_MINUTES)
        recent_events = [(t, m, la, lo) for (t, m, la, lo) in recent_events if t > cutoff]

        # Clear axes instead of creating new figures
        ax1.clear()
        ax2.clear()
        ax3.clear()
           
        # --- 1️⃣ Frequency plot ---
        xs, ys = compute_counts(recent_events)
        ax1.plot(xs, ys, color="tab:blue", linewidth=2)
        ax1.set_title("Earthquake Frequency (per minute)")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Count")
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        # --- 2️⃣ Histogram of magnitudes ---
        magnitudes = [m for _, m, *_ in recent_events]
        ax2.hist(magnitudes, bins=10, color="green", edgecolor="black")
        ax2.set_title("Magnitude Distribution")
        ax2.set_xlabel("Magnitude")
        ax2.set_ylabel("Count")

        # --- 3️⃣ Animated map ---
        ax3.set_xlim(-180, 180)
        ax3.set_ylim(-90, 90)
        ax3.set_title(f"Recent Earthquakes (last {WINDOW_MINUTES} min)")
        ax3.set_xlabel("Longitude")
        ax3.set_ylabel("Latitude")

        now = datetime.now()
        for (t, m, la, lo) in recent_events:
            age = (now - t).total_seconds()
            alpha = max(0.1, min(1, 1 - abs(age) / (WINDOW_MINUTES * 60)))
            ax3.scatter(lo, la, s=m**2, color="red", alpha=alpha)

            # --- Auto-save visualization every 60s ---
        if (datetime.now() - last_save_time).total_seconds() >= SAVE_INTERVAL:
            # Count total earthquakes processed
            quake_count = len(recent_events)

            # Increment snapshot index
            if "snapshot_index" not in globals():
                snapshot_index = 1
            else:
                snapshot_index += 1

            # Add label to the main figure title
            fig.suptitle(f"Snapshot #{snapshot_index} – {quake_count} Earthquakes Processed",
                         fontsize=12, fontweight="bold")

            # Build labeled filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"earthquake_viz_snapshot_{snapshot_index:03d}_{quake_count}quakes_{timestamp}.png"
            filepath = os.path.join("images", filename)

            # Save the figure
            plt.savefig(filepath)
            print(f"📸 Saved snapshot #{snapshot_index}: {filepath}")
            last_save_time = datetime.now()

        # --- Refresh the live figure every cycle ---
        plt.draw()
        plt.pause(0.5)


    except Exception as e:
        print("Error processing message:", e)
