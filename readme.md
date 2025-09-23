
# DriftMind Client

A Python client for interacting with the **DriftMind Forecasting Service**.
This package makes it easy to:

* Create and manage forecasters at scale
* Recover details and data managed by forecasters at any point
* Feed time-series data in real time
* Request predictions as feeding data and check system clusters
* Demonstrate DriftMind cold-start / continious training capabilities

---

## 🚀 Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/thingbook-io/driftmind-client.git
cd driftmind-client
pip install -e .
````

---

## ⚙️ Configuration

The client requires two pieces of information:

* **API key**
* **Base URL** of the DriftMind API (e.g. `https://api.thingbook.io/access/api/driftmind`)

These are typically stored in `resources/DRIFTMIND_CONNECT.txt`:

```
DRIFTMIND_API_KEY=your_api_key
DRIFTMIND_API_URL=https://api.thingbook.io/access/api/driftmind
```

---

## 📖 Usage

### 1. Import and connect

```python
from driftmind import DriftMindClient
from driftmind.generator import generate_sin_cos_tan_with_drifts
from driftmind.utils import extract_point_forecast

client = DriftMindClient(api_key, base_url)
```

---

### 2. Create a forecaster

```python
forecaster = client.create_forecaster({
    "forecasterName": "Cold Start Demo",
    "features": ["Sin", "Cos", "Tan"],
    "inputSize": 15,
    "outputSize": 1
})
fid = forecaster["forecaster_id"]
```

---

### 3. Feed data

Data must always be passed as arrays (`double[]` on the server side):

```python
data_point = {
    "Sin": [0.12],
    "Cos": [0.34],
    "Tan": [0.56]
}
client.feed_data(fid, data_point)
```

You can also batch multiple points:

```python
data_batch = {
    "Sin": [0.12, 0.13, 0.14],
    "Cos": [0.34, 0.35, 0.36],
    "Tan": [0.56, 0.57, 0.58]
}
client.feed_data(fid, data_batch)
```

---

### 4. Forecast

Once data has been fed, you can request a forecast.  
⚠️ The forecast operation can only be requested once there is **enough data**, meaning:

```

number of fed points ≥ inputSize + outputSize

````

```python
result = client.forecast(fid)
yhat = extract_point_forecast(result, target="Sin")

print("Predicted next Sin:", yhat)
````

---

#### 📦 Response Format

A successful forecast request returns a JSON object with both global metrics and per-feature results.

**Example response:**

```json
{
  "anomalyScore": 0.03,
  "numberOfClusters": 24,
  "FeaturesMap": {
    "Tan": {
      "timeStamps": ["23-09-2025 01:33:37"],
      "predictions": [-0.3633],
      "upperConfidence": [-0.1078],
      "lowerConfidence": [-1.8216],
      "anomalyScore": 0,
      "forecastingMethod": "Clustering",
      "numberOfClusters": 8
    },
    "Cos": {
      "timeStamps": ["23-09-2025 01:33:37"],
      "predictions": [1.5515],
      "upperConfidence": [1.7922],
      "lowerConfidence": [1.3251],
      "anomalyScore": 0.07,
      "forecastingMethod": "Clustering",
      "numberOfClusters": 8
    },
    "Sin": {
      "timeStamps": ["23-09-2025 01:33:37"],
      "predictions": [-0.0016],
      "upperConfidence": [0.2502],
      "lowerConfidence": [-0.2372],
      "anomalyScore": 0.01,
      "forecastingMethod": "Clustering",
      "numberOfClusters": 8
    }
  }
}
```

---

#### 🔑 Field Descriptions

* **`anomalyScore` (float)** – Global anomaly score across all features.
* **`numberOfClusters` (int)** – Total number of clusters currently maintained by the system.
* **`allResults` (object)** – Per-feature forecast results. Each feature (e.g. `Sin`, `Cos`, `Tan`) contains:

  * **`timeStamps` (list\[str])** – Timestamps of forecasted points.
  * **`predictions` (list\[float])** – Forecasted values.
  * **`upperConfidence` / `lowerConfidence` (list\[float])** – Confidence interval bounds.
  * **`anomalyScore` (float)** – Anomaly score specific to this feature.
  * **`forecastingMethod` (str)** – Forecasting approach used (e.g. `Clustering`, `Geometric`).
  * **`numberOfClusters` (int)** – Number of clusters contributing to this feature’s forecast.

---

#### 🔍 Example: Working with Forecasts

```python
# Access global anomaly score
print("Global anomaly score:", result["anomalyScore"])

# Iterate over feature forecasts
for feature, details in result["allResults"].items():
    print(f"\nFeature: {feature}")
    print("Predicted:", details["predictions"][0])
    print("Confidence interval:", (details["lowerConfidence"][0], details["upperConfidence"][0]))
    print("Feature anomaly score:", details["anomalyScore"])
```





---

### 5. Example: Cold-Start Demo

A demo notebook is included in `notebooks/cold_start_demo.ipynb` which:

* Creates a forecaster
* Generates synthetic `sin/cos/tan` data with drifts
* Feeds data point by point
* Requests forecasts in the loop
* Plots Actual vs Predicted for all three features

---

## 🧪 Development

Run tests with:

```bash
pytest
```

---

## 📜 License

MIT

