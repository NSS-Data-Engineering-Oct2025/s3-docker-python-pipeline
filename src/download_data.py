import os
import requests

from config import TAXI_DATA_URL, RAW_TAXI_FILE


def download_taxi_data():
    """
    Download NYC Taxi data and save it locally.
    """

    os.makedirs("data/raw", exist_ok=True)

    print("Downloading NYC Taxi dataset...")

    response = requests.get(TAXI_DATA_URL, stream=True)
    response.raise_for_status()

    with open(RAW_TAXI_FILE, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"File saved to: {RAW_TAXI_FILE}")


if __name__ == "__main__":
    download_taxi_data()