import os
import requests
from dotenv import load_dotenv
import io
import polars as pl
import time
from utils import write_data_to_minio
from db_sync import db_sync
from logger import setup_logging
logger = setup_logging()
load_dotenv()

def fetch_api_data(base_url):
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.content
    dataframe = pl.read_csv(io.BytesIO(data))
    result = dataframe
    return result


    
def convert_dataframe_to_parquet(dataframe):
    buffer = io.BytesIO()
    try:
        dataframe.write_parquet(buffer)
        buffer.seek(0)
        result = buffer
        return result
    except Exception as e:
        logger.error(f"Failed to convert DataFrame to Parquet in-memory: {e}")
        return None


def data_ingestion():
    tick = time.time()
    minio_bucket = os.getenv("MINIO_BUCKET_NAME")
    ondoriya_url = os.getenv("BASE_URL")

    FILES_TO_INGEST = [
    "faction_distribution.csv",
    "households.csv",
    "language_building_blocks.csv",
    "language_roots.csv",
    "moons.csv",
    "people.csv",
    "planets.csv",
    "region_biome.csv",
    "regions.csv"
]

    for path in FILES_TO_INGEST:
        logger.info(f"Fetching Ondoriya Data from {path}")
        path_dataframe = fetch_api_data(f"{ondoriya_url}/{path}")
        path_parquet_buffer = convert_dataframe_to_parquet(path_dataframe)
        logger.info("Writing Ondoriya Data to MinIO Storage")
        path_file = os.path.splitext(path)[0] + ".parquet"
        write_data_to_minio(path_parquet_buffer, minio_bucket, path_file, "RAW")

    tock = time.time() - tick

    logger.info("Synchronizing Data to Database")
    db_sync()

    logger.info(f"Data ingestion completed in {tock:.2f} seconds.")