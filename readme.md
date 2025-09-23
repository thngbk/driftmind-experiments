

# DriftMind Client

DriftMind is an **adaptive forecasting and anomaly detection engine** designed for **fast, real-time data environments**.  
Unlike traditional forecasting systems that require long offline training phases, DriftMind uses an **online training approach**: it learns continuously from incoming data streams and can start generating forecasts as soon as enough points are fed.

---

## ✨ Why DriftMind?

DriftMind is particularly well-suited for:

- 🌐 **Streaming data scenarios** such as telecom, IoT, or finance  
- ⚡ **Cold-start forecasting** — predictions available immediately without long historical training  
- 🔍 **On-the-fly anomaly detection** using dynamic clustering  
- 📈 **Scalable deployments** where thousands of forecasters can be created, queried, and updated in real time  

---

## 🔬 Core Concepts

At its core, DriftMind blends:

- **Online clustering** to adapt quickly to new patterns  
- **Geometric forecasting** as a fallback when no cluster is available  
- **Continuous learning** without explicit retraining steps  

---

## 🎯 What the Python Client Does

The **DriftMind Client** is a lightweight Python package that makes it easy to:

- Create and manage forecasters at scale  
- Stream time-series data point by point or in batches  
- Request forecasts, anomaly scores, and cluster insights at any time  
- Visualize actual vs predicted values, anomaly scores, and cluster evolution  

---

With DriftMind, forecasting becomes a **live, adaptive process** — not a static one.


---

## 🛠 Prerequisites

Before using the DriftMind Client, make sure you have the following:

### 1. Python environment
- Python **3.8+**  
- [pip](https://pip.pypa.io/en/stable/) for installing dependencies  

The package depends on:
- `requests`
- `pandas`
- `matplotlib` (for visualization utilities)

All dependencies will be installed automatically via `pip install -e .`.

---

### 2. DriftMind backend service
The client communicates with the **DriftMind API service**.  
You will need either:
- Access to a **Thingbook.io hosted DriftMind endpoint**, or  
- A **local deployment** of the DriftMind backend (Kubernetes) if you are running Thingbook Backend on-prem.  

Without a running DriftMind API, the client cannot create forecasters or request forecasts.

---

### 3. API credentials
You need:
- **API key** (provided by your DriftMind deployment)  
- **Base URL** of the DriftMind API (e.g. `https://api.thingbook.io/access/api/driftmind`)  

These are usually stored in `resources/DRIFTMIND_CONNECT.txt`:

---

## 🚀 Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/thngbk/driftmind.git
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

### 2. Create a Forecaster

A **forecaster** is the core unit in DriftMind: it maintains its own state, learns continuously from the data you feed, and produces forecasts, anomaly scores, and cluster information.

---

#### 🟢 Minimum configuration

At minimum, you only need to specify:

- **`forecasterName`** – A human-friendly name for the forecaster  
- **`features`** – A list of feature names (columns in your dataset)  
- **`inputSize`** – Number of past points used as input  
- **`outputSize`** – Number of future points to forecast  

Example:

```python
forecaster = client.create_forecaster({
    "forecasterName": "Cold Start Demo",
    "features": ["Sin", "Cos", "Tan"],
    "inputSize": 15,
    "outputSize": 1
})
fid = forecaster["forecaster_id"]
```

If only these parameters are provided, DriftMind applies sensible defaults for the rest.

---

#### ⚙️ Extended configuration

You can override defaults to fine-tune behavior.

**Full example:**

```python
forecaster = client.create_forecaster({
  "forecasterName": "Machine Health Forecaster",
  "features": ["vibration_g", "motor_temp_c", "power_kw"],
  "inputSize": 30,
  "outputSize": 1,
  "maxClustersAllowed": 50,
  "similarityThreshold": 0.8,
  "timeStampIntervalInSeconds": 30,
  "fitRate": 1,
  "useCustomDateFormat": True,
  "dateFormat": "dd-MM-yyyy HH:mm",
  "useInitializationDate": True,
  "initializationDate": "01-01-2025 00:00"
})
fid = forecaster["forecaster_id"]
```

---

#### 📋 Parameter Reference

| Parameter                    | Type   | Required | Default                            | Description                                                  |
| ---------------------------- | ------ | -------- | ---------------------              | ------------------------------------------------------------ |
| `forecasterName`             | string | ✅ Yes    | –                                 | Human-readable name for the forecaster.                     |
| `features`                   | list   | ✅ Yes    | –                                 | List of feature names (columns in your dataset).            |
| `inputSize`                  | int    | ✅ Yes    | –                                 | Number of past points used as input.                        |
| `outputSize`                 | int    | ✅ Yes    | –                                 | Number of future points to forecast.                        |
| `maxClustersAllowed`         | int    | No         | 200                              | Maximum number of clusters maintained.                       |
| `similarityThreshold`        | float  | No        | 0.8                               | Similarity threshold (0–1) for assigning points to clusters. |
| `timeStampIntervalInSeconds` | int    | No        | 60                                | Expected interval between points expressed in Seconds        |
| `fitRate`                    | int    | No        | 1                                 | Frequency of model updates (lower = faster adaptation).     |
| `useCustomDateFormat`        | bool   | No        | False                             | Whether to parse timestamps with a custom format.            |
| `dateFormat`                 | string | No        | `yyyy-MM-dd HH:mm:ss`             | Date format when `useCustomDateFormat` is true.              |
| `useInitializationDate`      | bool   | No        | False                             | Whether to align forecasts relative to a given start date.   |
| `initializationDate`         | string | No        | System time at Forecaster Creation| Explicit start date.        |

---

With this flexibility, you can start with **minimal setup for quick prototyping**, and later move to **fine-grained configurations** for production scenarios like industrial IoT, telecom, or financial forecasting.



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

One of the key characteristics of **DriftMind** is its **online training approach**. This means there is no need for a formal training phase before requesting forecasts, the model begins learning as soon as data starts flowing in.

The only requirement for generating a forecast is that a **minimum number of points** must be fed into the system. This number is simply the sum of the **input length** and the **output length**.

For example, if the forecaster is configured with an input length of 20 and an output length of 5, the system must first receive **25 points** before it can produce a valid forecast. Once this threshold is reached, DriftMind can start delivering predictions in real time while continuously updating its internal models as new data arrives.

---

```
Minimum required points = Input length + Output length

    |<---------------------------- Input (20 points) ------------------------->|<Output (5 points)>|
---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●---●
                                                                                                   ^ Forecast starts here
```

---


```python
#Forecaster Features
columns = ["Sin", "Cos", "Tan"]

#Request forecasting Data
result = client.forecast(fid)

# Visualize results
for var in columns:
    df_var = pd.DataFrame(results[var])
    utils.plot_actual_vs_predicted(df_var, var)
```
![alt text](images/image.pngimage.png)
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
* **`FeaturesMap` (object)** – Per-feature forecast results. Each feature (e.g. `Sin`, `Cos`, `Tan`) contains:
  * **`timeStamps` (list\[str])** – Timestamps of forecasted points.
  * **`predictions` (list\[float])** – Forecasted values.
  * **`upperConfidence` / `lowerConfidence` (list\[float])** – Confidence interval bounds.
  * **`anomalyScore` (float)** – Anomaly score specific to this feature.
  * **`forecastingMethod` (str)** – Forecasting approach used (e.g. `Clustering`, `Extension`, `Naive`).
  * **`numberOfClusters` (int)** – Number of clusters active in the system for this Forecaster. the clusters model the recent and past beheviour with minimum footprint.

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

### 5. Recover forecaster data

At any time, you can inspect the **data currently held by a forecaster**.  
This is useful for debugging, validation, or verifying that data points are being stored correctly.

```python
data_snapshot = client.get_forecaster_data(fid)

if data_snapshot:
    for ts, values in data_snapshot["data"].items():
        print(f"{ts} → {values}")
```
Example response. Each key in the data object is a timestamp, and its value is a dictionary containing the last known values for each feature.
```json
{
  "data": {
    "23-09-2025 18:54:20": { "Tan": -0.8335, "Sin": -0.6755, "Cos": 0.3708 },
    "23-09-2025 18:55:20": { "Tan": -0.7879, "Sin": -0.6472, "Cos": 0 },
    "23-09-2025 18:56:20": { "Tan": -0.7458, "Sin": -0.6164, "Cos": -0.3708 },
    "23-09-2025 18:57:20": { "Tan": -0.7067, "Sin": -0.5832, "Cos": -0.7053 },
    "23-09-2025 18:58:20": { "Tan": -0.6703, "Sin": -0.5476, "Cos": -0.9708 }
  }
}

```

### 6. List all forecasters

You can query the system to get a list of all available forecasters. Each entry contains metadata such as the forecaster’s ID, name, creation date, and usage stats.

```python
all_forecasters = client.list_forecasters()

if all_forecasters:
    for f in all_forecasters:
        print(f"ID={f['objectId']}, Name={f['objectName']}, Created={f['createdAt']}, Requests={f['requestsProcessed']}")
```


Example Response: 
```json

[
  {
    "objectId": "a82bdf13-becf-4a06-9c97-c7b106a8fbac",
    "objectName": "Cold Start Demo",
    "createdAt": "2025-09-22",
    "createdBy": "VfYZ3hLQk6FohdPTkKXB0lC30DworzI5Mz0M2NTk1MDY3MjE4MDE4NDwE3MTA3OTA1NDUzMDc4Njg5NjA0Nw",
    "objectType": "FORECASTER",
    "dataProcessed": "-0.67",
    "requestsProcessed": "601"
  },
  {
    "objectId": "c339beb7-ae9b-4f3e-bb73-e4d4245cb507",
    "objectName": "Basic Forecaster Creation",
    "createdAt": "2025-09-22",
    "createdBy": "VfYZ3hLQk6FohdPTkKXB0lC30DworzI5Mz0M2NTk1MDY3MjE4MDE4NDwE3MTA3OTA1NDUzMDc4Njg5NjA0Nw",
    "objectType": "FORECASTER",
    "dataProcessed": "-3.19",
    "requestsProcessed": "1202"
  }
]
```
Each element in the list includes:

* **objectId** – Unique ID of the forecaster  
* **objectName** – Human-readable name  
* **createdAt** – Date of creation  
* **createdBy** – API key used to create the forecaster  
* **objectType** – Always `"FORECASTER"` for these objects  
* **dataProcessed** – Amount of data processed (aggregate value) in MB. This value will be always negative  
* **requestsProcessed** – Number of requests served by the forecaster  


---

### 8. Get forecaster details

You can inspect the **configuration and properties of a specific forecaster** using its ID.  
This is useful for verifying feature setup, parameters, and metadata.

```python
fid = "529cd364-67b2-4f04-8c07-c42b5740b3aa"
details = client.get_forecaster_details(fid)

if details:
    print("Forecaster Name:", details["forecasterName"])
    print("Features:", details["features"])
    print("Input Size:", details["properities"]["inputSize"])
    print("Output Size:", details["properities"]["outputSize"])
```

Example response:

```json
{
  "features": ["Tan", "Sin", "Cos"],
  "properities": {
    "fitRate": "1",
    "initializationDate": "23-09-2025 09:37:13",
    "maxClustersAllowed": "100",
    "dateFormat": "dd-MM-yyyy HH:mm:ss",
    "similarityThreshold": "0.8",
    "timeStampIntervalInSeconds": "60",
    "outputSize": "1",
    "inputSize": "15"
  },
  "forecasterId": "529cd364-67b2-4f04-8c07-c42b5740b3aa",
  "forecasterName": "Cold Start Demo"
}
```

---
### 9. Example: Cold-Start Demo

A demo notebook is included in `notebooks/cold_start_demo.ipynb` which:

* Creates a forecaster
* Generates synthetic `sin/cos/tan` data with drifts
* Feeds data point by point
* Requests forecasts in the loop
* Plots Actual vs Predicted for all three features

---

## 📜 License

MIT

