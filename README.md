# Earthquake Streaming Project (P6)

This project continues the earthquake-themed streaming pipeline developed in earlier Buzzline assignments.  
It demonstrates how to organize a real-time data engineering project using producers, consumers, and a local database.

---

## Environment

- **Operating System:** Windows 10 using **WSL2 (Ubuntu 22.04)**  
- **Editor:** Visual Studio Code (with WSL:Ubuntu integration)  
- **Python Environment:** `.venv` virtual environment created inside WSL  
- **Dependencies:** See `requirements.txt`  

To recreate the environment:
```bash
# Clone the repo into WSL
git clone https://github.com/14dstcyr/buzzline-06-stcyr.git
cd buzzline-06-stcyr

# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
