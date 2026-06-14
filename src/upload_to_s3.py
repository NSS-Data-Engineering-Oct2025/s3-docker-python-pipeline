import os
import boto3

from config import AWS_PROFILE, S3_BUCKET, S3_PREFIX, PROCESSED_FOLDER


def upload_processed_files_to_s3():
    """
    Upload all processed CSV files to the project folder in S3.
    """

    session = boto3.Session(profile_name=AWS_PROFILE, region_name="us-east-2")
    s3_client = session.client("s3")

    for file_name in os.listdir(PROCESSED_FOLDER):
        local_file_path = os.path.join(PROCESSED_FOLDER, file_name)

        if os.path.isfile(local_file_path):
            s3_key = f"{S3_PREFIX}/processed/{file_name}"

            print(f"Uploading {local_file_path} to s3://{S3_BUCKET}/{s3_key}")
            s3_client.upload_file(local_file_path, S3_BUCKET, s3_key)

    print("Upload complete.")


if __name__ == "__main__":
    upload_processed_files_to_s3()