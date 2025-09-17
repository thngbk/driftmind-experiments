# DriftMind Experiments

This repository contains public notebooks, datasets, and scripts that demonstrate how to use the [DriftMind](https://thingbook.io) API for time series forecasting and anomaly detection.

## 🚀 What is DriftMind?

DriftMind is a real-time, adaptive forecasting engine designed for high-speed environments where patterns drift over time. It supports anomaly detection and time series forecasting through lightweight REST APIs.

## 📁 Structure

- `notebooks/`: Jupyter notebooks for different use cases
- `data/`: Sample datasets used in experiments
- `resources/`: Placeholder for config files (e.g., API keys, environment)
- `scripts/`: Optional preprocessing or utilities
- `.env.example`: Example environment configuration

## 📦 Setup

```bash
git clone https://github.com/thingbookio/driftmind-experiments.git
cd driftmind-experiments
python -m venv venv
source venv/bin/activate     # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env         # Then edit .env with your API key
