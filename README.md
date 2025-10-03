# Earthquake Streaming Project (P6) Progression

This repository documents the progression of a custom earthquake‑themed streaming pipeline project through CC6.1 → CC6.2 → CC6.3 → P6. Each checkpoint builds toward a more advanced, real‑time analytics system using Kafka, SQLite, and dynamic visualization.

---

## CC6.1 – Kickoff & Connections

- Focus: Set up the initial streaming project with environment prep.

- Key Work: Verified WSL2 + VS Code integration, created .venv, connected Kafka, and established folder structure (producers/, consumers/, utils/, data/).

- Outcome: Ready foundation for building earthquake streaming components.

## CC6.2 – Getting Started

- Focus: Create the first producer and consumer scripts.

- Producer: Generated simple earthquake‑like messages (JSON/CSV) and published them to a Kafka topic.

- Consumer: Subscribed, read messages, and stored them into SQLite.

- Outcome: Proved end‑to‑end pipeline works with simulated data.

## CC6.3 – Earthquake Streaming Project

- Focus: Expand to visualize earthquake events.

- Producer: Continued using earthquake‑themed messages (simulated).

- Consumer: Stored messages in SQLite and displayed dynamic Matplotlib charts (rolling counts, magnitude plots).

- Challenges: Adjusting chart sizing and animation refresh while messages streamed.

- Outcome: Interactive consumer that made earthquake activity visible in near‑real‑time.

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

### Setup Commands
```bash
git clone https://github.com/14dstcyr/buzzline-06-earthquake-stcyr.git
cd buzzline-06-earthquake-stcyr
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root with:
```
EARTHQUAKE_TOPIC=eq-topic
```

### Running the project
#### For CC6.1 - CC6.3

#### 1. Start ZooKeeper and Kafka Broker (in separate terminals):
```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
````

#### 2. Run the **basic producer** (generates earthquake messages):
```
python earthquake_producer_stcyr.py
```

#### 3. Run the **basic consumer** (prints events to console):
```
python earthquake_consumer_stcyr.py
```

#### 4. Run the **consumer with visualization** (real-time charts):
```
python earthquake_consumer_viz_stcyr.py
```

### For P6 (Final Project)
- **Terminal A – Start Producer**
  ```
  source .venv/bin/activate
  python producers/producer_usgs_stcyr.py
  ```

- **Terminal B – Start Consumer (opens live chart)**
  ```
  source .venv/bin/activate
  python consumers/consumer_stcyr.py
  ```


### Dataflow
```
flowchart LR
    A[Producer: earthquake_producer_stcyr.py] -->|JSON events| B[(Kafka Topic: eq-topic)]
    B --> C[Consumer: earthquake_consumer_stcyr.py]
    B --> D[Consumer with Viz: earthquake_consumer_viz_stcyr.py]
    D --> E[📈 Line Chart: Magnitudes]
    D --> F[📊 Bar Chart: Counts by Location]
```
