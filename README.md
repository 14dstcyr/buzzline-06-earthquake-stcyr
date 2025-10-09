# Earthquake Streaming Project (P6-P7) Progression

This project builds upon the earthquake-themed streaming pipeline developed across previous Buzzline assignments (CC6–CC7).
It demonstrates real-time data ingestion, analysis, and visualization using a Kafka producer–consumer pipeline.

The final version introduces enhanced data visualizations, automatic chart snapshots, and sliding-window analysis.

---

## Environment Setup

- Operating System: Windows 11 using WSL 2 (Ubuntu 22.04)

- Editor: Visual Studio Code (with “WSL: Ubuntu” integration)

- Python Version: 3.11

- Virtual Environment: .venv

## CC6.1 – Kickoff & Connections

- **Focus**: Set up the initial streaming project with environment prep.

- **Key Work**: Verified WSL2 + VS Code integration, created .venv, connected Kafka, and established folder structure (producers/, consumers/, utils/, data/).

- **Outcome**: Ready foundation for building earthquake streaming components.

## CC6.2 – Getting Started

- **Focus**: Create the first producer and consumer scripts.

- **Producer**: Generated simple earthquake‑like messages (JSON/CSV) and published them to a Kafka topic.

- **Consumer**: Subscribed, read messages, and stored them into SQLite.

- **Outcome**: Proved end‑to‑end pipeline works with simulated data.

## CC6.3 – Earthquake Streaming Project

- **Focus**: Expand to visualize earthquake events.

- **Producer**: Continued using earthquake‑themed messages (simulated).

- **Consumer**: Stored messages in SQLite and displayed dynamic Matplotlib charts (rolling counts, magnitude plots).

- **Challenges**: Adjusting chart sizing and animation refresh while messages streamed.

- **Outcome**: Interactive consumer that made earthquake activity visible in near‑real‑time.

## P6 – Custom Streaming Pipeline (Final Project)

New Feature: Live earthquake data ingestion from USGS + rolling seismic energy visualization.

### Overview

This custom streaming pipeline fetches live earthquake events from the **USGS GeoJSON feed**, publishes them to Kafka (producer), consumes and stores them in SQLite (consumer), and computes a **rolling 60‑minute seismic energy metric** that is rendered as a dynamic Matplotlib animation.

### Key Components

- **Producer (USGS → Kafka)**: Polls USGS feed, deduplicates events, and publishes JSON to Kafka.

- **Consumer (Kafka → SQLite + Visualization)**:

    - Stores events into SQLite.

    - Converts magnitudes to seismic moment (energy proxy).

    - Maintains a 60‑minute rolling window of total energy and counts of ≥4.0 magnitude events.

    - Animates log10(total energy) with annotations for latest event.


### Insight

- Energy‑based visualization shows bursts of seismic activity that simple counts miss.

- Annotated charts highlight latest event details + rolling counts of ≥4.0 magnitude events.

### Challenges & Lessons Learned

- Getting smooth live animation while consuming and writing to SQLite.

- Balancing GUI refresh with streaming ingestion.

- Importance of deduplication and window pruning.



## Environment Setup (applies to all checkpoints)

- **Operating System**: Windows 11 using WSL2 (Ubuntu 22.04)

- **Editor**: Visual Studio Code (with WSL:Ubuntu integration)

- **Python Environment**: .venv virtual environment created inside WSL

- **Dependencies**: See requirements.txt

### Environment Setup Commands
```bash
# Navigate to project folder
cd ~/projects/buzzline-06-earthquake-stcyr

# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root with:
```
EARTHQUAKE_TOPIC=eq-topic
```

## Streaming Pipeline Overview
### Producer – earthquake_producer_stcyr.py

- Connects to Kafka at localhost:9092

- Publishes simulated earthquake events to the topic defined in .env

- Each event includes:

    - id

    - magnitude

    - location

    - depth_km

### Consumer – earthquake_consumer_stcyr.py

- Subscribes to the same Kafka topic

- Continuously reads live messages

- Parses and stores recent events in a sliding 5-minute window

- Generates three dynamic visualizations that update in real time

## New Features for P7
### Automatic Labeled Snapshots
- The consumer now saves high-resolution PNG images automatically every 60 seconds.

- Each file includes a title and labeled filename, e.g.
```bash
images/earthquake_viz_snapshot_003_18quakes_20251009_142612.png
```
- Titles in saved charts show snapshot number and total earthquakes processed.

### Fully Automated Visualization Updates
- The charts refresh every 2 seconds with new Kafka messages.

- The visualization resets cleanly between frames for smooth performance.

### Sliding-Window Data Management
- Keeps only the last 5 minutes of earthquake data in memory.

- Prevents clutter and enables a live “moving window” effect.

### Improved Stability
- Optional use of `plt.clf()` for full figure refreshes to avoid ghosting.

- Automatic creation of the `/images` folder if missing.

- Built-in error handling for incomplete or missing data fields.

### Running the project
#### 1. Start ZooKeeper and Kafka Broker (if applicable)(in separate terminals):
```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
````

#### 2. Run the producer in a new terminal (generates earthquake messages):
```
source .venv/bin/activate
python earthquake_producer_stcyr.py
```

#### 3. Run the consumer in a new terminal (prints events to console):
```
source .venv/bin/activate
python earthquake_consumer_stcyr.py
```


## Visualizations

### Time Series of Earthquake Frequency (per minute)
Displays the count of earthquake events per minute in the last 5 minutes.
Helps visualize short-term seismic activity patterns.

## Histogram of Magnitudes
Shows the distribution of earthquake magnitudes in the current time window.
Helps identify the relative frequency of weaker vs. stronger events.

## Animated World Map (Sliding Window)
Plots recent earthquakes by latitude / longitude on a simplified global map.
Older points fade gradually to highlight new activity.




## Final Notes

### This project demonstrates:

- Real-time streaming data ingestion with Apache Kafka

- Sliding-window analytics
    
- Multi-panel visualization with Matplotlib
    
- Environment management with .env and .venv
    
- Automated documentation through periodic image saving
