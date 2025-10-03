# Earthquake Streaming Project (P6)

This project continues the earthquake-themed streaming pipeline from earlier Buzzline assignments.  
It demonstrates how to organize and initialize a real-time data project with Kafka producers and consumers, storing 
messages in SQLite for analysis and visualization.


---

## Environment Setup

- **Operating System:** Windows 11 using **WSL2 (Ubuntu 22.04)**  
- **Editor:** Visual Studio Code (with WSL:Ubuntu integration)  
- **Python Environment:** `.venv` virtual environment created inside WSL  
- **Dependencies:** See `requirements.txt`  

To recreate the environment:
```bash
# Clone the repo into WSL
git clone https://github.com/14dstcyr/buzzline-06-earthquake-stcyr.git
cd buzzline-06-earthquake-stcyr

## Environment Variables

Create a `.env` file in the project root with:

EARTHQUAKE_TOPIC=eq-topic

# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

flowchart LR
    A[Producer: earthquake_producer_stcyr.py] -->|JSON events| B[(Kafka Topic: eq-topic)]
    B --> C[Consumer: earthquake_consumer_stcyr.py]
    B --> D[Consumer with Viz: earthquake_consumer_viz_stcyr.py]
    D --> E[📈 Line Chart: Magnitudes]
    D --> F[📊 Bar Chart: Counts by Location]
