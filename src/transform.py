import os
import pandas as pd

from config import RAW_TAXI_FILE, PROCESSED_FOLDER


def transform_taxi_data():
    """
    Read raw NYC Taxi parquet data, clean it, and create summary output files.
    """

    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    print("Reading raw taxi data...")
    taxi_data = pd.read_parquet(RAW_TAXI_FILE)

    print(f"Raw rows: {len(taxi_data)}")

    selected_columns = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "fare_amount",
        "tip_amount",
        "total_amount",
        "payment_type",
    ]

    taxi_data = taxi_data[selected_columns].copy()

    taxi_data = taxi_data.dropna()

    taxi_data = taxi_data[
        (taxi_data["trip_distance"] > 0)
        & (taxi_data["fare_amount"] > 0)
        & (taxi_data["total_amount"] > 0)
    ]

    taxi_data["pickup_date"] = taxi_data["tpep_pickup_datetime"].dt.date
    taxi_data["trip_duration_minutes"] = (
        taxi_data["tpep_dropoff_datetime"] - taxi_data["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    taxi_data = taxi_data[
        (taxi_data["trip_duration_minutes"] > 0)
        & (taxi_data["trip_duration_minutes"] <= 180)
    ]

    cleaned_file = f"{PROCESSED_FOLDER}/cleaned_taxi_trips.csv"
    daily_summary_file = f"{PROCESSED_FOLDER}/daily_trip_summary.csv"
    payment_summary_file = f"{PROCESSED_FOLDER}/payment_type_summary.csv"

    taxi_data.to_csv(cleaned_file, index=False)

    daily_summary = (
        taxi_data.groupby("pickup_date")
        .agg(
            total_trips=("pickup_date", "count"),
            average_distance=("trip_distance", "mean"),
            average_fare=("fare_amount", "mean"),
            total_revenue=("total_amount", "sum"),
            average_tip=("tip_amount", "mean"),
        )
        .reset_index()
    )

    daily_summary.to_csv(daily_summary_file, index=False)

    payment_summary = (
        taxi_data.groupby("payment_type")
        .agg(
            total_trips=("payment_type", "count"),
            average_fare=("fare_amount", "mean"),
            average_tip=("tip_amount", "mean"),
            total_revenue=("total_amount", "sum"),
        )
        .reset_index()
    )

    payment_summary.to_csv(payment_summary_file, index=False)

    print(f"Cleaned rows: {len(taxi_data)}")
    print("Processed files created:")
    print(cleaned_file)
    print(daily_summary_file)
    print(payment_summary_file)


if __name__ == "__main__":
    transform_taxi_data()