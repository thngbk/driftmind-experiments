
# DriftMind Client

A Python client for interacting with the **DriftMind Forecasting API**.
This package makes it easy to:

* Create and manage forecasters
* Feed time-series data
* Request predictions
* Demonstrate DriftMind capabilities

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
* **Base URL** of the DriftMind API (e.g. `http://localthingbook.io:32081/access/api/driftmind`)

These are typically stored in `resources/DRIFTMIND_CONNECT.txt`:

```
DRIFTMIND_API_KEY=your_api_key
DRIFTMIND_API_URL=http://localthingbook.io:32081/access/api/driftmind
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
    "features": ["Sin", "Cos", "Tan", "Sequence"],
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
    "Tan": [0.56],
    "Sequence": [42]
}
client.feed_data(fid, data_point)
```

You can also batch multiple points:

```python
data_batch = {
    "Sin": [0.12, 0.13, 0.14],
    "Cos": [0.34, 0.35, 0.36],
    "Tan": [0.56, 0.57, 0.58],
    "Sequence": [42, 43, 44]
}
client.feed_data(fid, data_batch)
```

---

### 4. Forecast

```python
result = client.forecast(fid)
yhat = extract_point_forecast(result, target="Sin")

print("Predicted next Sin:", yhat)
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

