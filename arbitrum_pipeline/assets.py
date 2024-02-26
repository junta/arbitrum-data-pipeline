from time import sleep
import requests
import pandas as pd
from dagster import AssetKey, asset
import os


@asset
def fetch_forum_topics() -> pd.DataFrame:
    url = "https://forum.arbitrum.foundation/latest.json"
    topics = []
    page = 1

    while True:
        params = {'page': page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        page_topics = data.get("topic_list", {}).get("topics", [])
        print(page)
        
        if not page_topics:
            break
        
        topics.extend(page_topics)    
        page += 1
        sleep(1)

    print(topics)
    df = pd.DataFrame(topics)
    return df


@asset
def materialized_forum_topics(fetch_forum_topics: pd.DataFrame) -> None:
    folder_name = 'output_data'

    csv_file_name = "topics.csv"
    csv_file_path = os.path.join(folder_name, csv_file_name)
    fetch_forum_topics.to_csv(csv_file_path, index=False)
    print(f"Data exported to CSV file: {csv_file_name}")
    
    # parquet_file_name = "topics.parquet"
    # parquet_file_path = os.path.join(folder_name, parquet_file_name)
    # fetch_forum_topics.to_parquet(parquet_file_path, index=False)
    # print(f"Data exported to Parquet file: {parquet_file_name}")