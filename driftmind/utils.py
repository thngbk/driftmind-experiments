import matplotlib.pyplot as plt
from pathlib import Path

def plot_actual_vs_predicted(df, variable_name):
    if df.empty:
        print(f"No data to plot for {variable_name}")
        return
    
    plt.figure(figsize=(15, 4))
    plt.plot(df["timestamp"], df["expected"], label="Actual", linewidth=2)
    plt.plot(df["timestamp"], df["predicted"], label="Predicted", linestyle='--')
    plt.title(f"{variable_name}: Actual vs Predicted")
    plt.xlabel("Time Step")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def load_credentials(filepath=Path("../resources/DRIFTMIND_CONNECT.txt")):
        credentials = {}

        try:
            with filepath.open("r") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        credentials[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Error: credentials file not found at {filepath}")
            return False

        # check required keys
        api_key = credentials.get("DRIFTMIND_API_KEY")
        base_url = credentials.get("DRIFTMIND_API_URL")

        if not api_key or not base_url:
            print("Error: Missing DRIFTMIND_API_KEY or DRIFTMIND_API_URL in credentials file.")
            return False

        return credentials