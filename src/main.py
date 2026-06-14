from download_data import download_taxi_data
from transform import transform_taxi_data
from upload_to_s3 import upload_processed_files_to_s3


def run_pipeline():
    """
    Run the full NYC Taxi ETL pipeline.
    """

    print("Starting NYC Taxi ETL Pipeline...")

    print("Step 1: Downloading raw data...")
    download_taxi_data()

    print("Step 2: Transforming data...")
    transform_taxi_data()

    print("Step 3: Uploading processed files to S3...")
    upload_processed_files_to_s3()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()