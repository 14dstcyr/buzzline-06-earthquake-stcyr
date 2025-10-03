# Earthquake Streaming Project (P6)

This project continues the earthquake-themed streaming pipeline from earlier Buzzline assignments.  
It demonstrates how to organize and initialize a real-time data project with Kafka producers and consumers,  
storing messages in SQLite for analysis and visualization.

---

## Environment Setup

- **Operating System:** Windows 11 using **WSL2 (Ubuntu 22.04)**  
- **Editor:** Visual Studio Code (with WSL:Ubuntu integration)  
- **Python Environment:** `.venv` virtual environment created inside WSL  
- **Dependencies:** See `requirements.txt`  

### Clone the repository
```bash
git clone https://github.com/14dstcyr/buzzline-06-earthquake-stcyr.git
cd buzzline-06-earthquake-stcyr

# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## Environment Variables

Create a `.env` file in the project root with:
EARTHQUAKE_TOPIC=eq-topic

### Running the project

#### 1. Start ZooKeeper and Kafka Broker (in separate terminals):
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties

#### 2. Run the Producer (generates earthquake messages):
python earthquake_producer_stcyr.py

#### 3. Run the Consumer (prints events to console):
python earthquake_consumer_stcyr.py

#### 4. Run the Consumer with Visualization (real-time charts):
python earthquake_consumer_viz_stcyr.py


### Dataflow

flowchart LR
    A[Producer: earthquake_producer_stcyr.py] -->|JSON events| B[(Kafka Topic: eq-topic)]
    B --> C[Consumer: earthquake_consumer_stcyr.py]
    B --> D[Consumer with Viz: earthquake_consumer_viz_stcyr.py]
    D --> E[📈 Line Chart: Magnitudes]
    D --> F[📊 Bar Chart: Counts by Location]
