from download_data import download_taxi_data
from transform import transform_taxi_data
from upload_to_s3 import upload_processed_files_to_s3
from logger import get_logger

logger = get_logger()


def run_pipeline():

    logger.info("Starting NYC Taxi ETL Pipeline")

    logger.info("Step 1: Downloading data")
    download_taxi_data()

    logger.info("Step 2: Transforming data")
    transform_taxi_data()

    logger.info("Step 3: Uploading files to AWS S3")
    upload_processed_files_to_s3()

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()