# NYC Taxi ETL Pipeline with AWS S3 and Docker

## Project Overview

This project is an end-to-end Data Engineering pipeline built with Python, Docker, AWS S3, and GitHub.

The pipeline downloads real NYC Yellow Taxi trip data, cleans and transforms the dataset, creates summary reports, saves optimized Parquet output, and uploads processed files to an AWS S3 bucket.

## Technologies Used

- Python
- Pandas
- PyArrow
- Boto3
- AWS S3
- AWS SSO
- Docker Desktop
- Docker Compose
- Git and GitHub
- VS Code

## Dataset

Dataset: NYC Yellow Taxi Trip Records  
Month: January 2024  
Raw Records: 2,964,624  
Cleaned Records: 2,752,466  

## Pipeline Steps

1. Download raw NYC Taxi Parquet data
2. Clean invalid trips
3. Calculate trip duration
4. Create cleaned CSV and Parquet outputs
5. Create daily trip summary
6. Create payment type summary
7. Upload processed files to AWS S3
8. Run pipeline locally or inside Docker

## Project Structure

```text
s3-docker-python-pipeline/
├── src/
│   ├── config.py
│   ├── download_data.py
│   ├── logger.py
│   ├── main.py
│   ├── transform.py
│   └── upload_to_s3.py
├── data/
│   ├── raw/
│   └── processed/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .gitignore
└── .dockerignore