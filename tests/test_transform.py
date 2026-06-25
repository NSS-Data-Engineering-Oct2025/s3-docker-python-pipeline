import os
import sys
import pandas as pd

# Add the src folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from transform import transform_taxi_data


def test_transform_creates_output_files():
    """
    Verify that the transform step creates all expected output files.
    """

    transform_taxi_data()

    assert os.path.exists("data/processed/cleaned_taxi_trips.csv")
    assert os.path.exists("data/processed/cleaned_taxi_trips.parquet")
    assert os.path.exists("data/processed/daily_trip_summary.csv")
    assert os.path.exists("data/processed/payment_type_summary.csv")


def test_cleaned_dataset_has_rows():
    """
    Verify the cleaned dataset is not empty.
    """

    dataframe = pd.read_parquet("data/processed/cleaned_taxi_trips.parquet")

    assert len(dataframe) > 0


def test_no_negative_fares():
    """
    Verify there are no negative fares.
    """

    dataframe = pd.read_parquet("data/processed/cleaned_taxi_trips.parquet")

    assert (dataframe["fare_amount"] >= 0).all()


def test_no_negative_distances():
    """
    Verify there are no negative trip distances.
    """

    dataframe = pd.read_parquet("data/processed/cleaned_taxi_trips.parquet")

    assert (dataframe["trip_distance"] >= 0).all()