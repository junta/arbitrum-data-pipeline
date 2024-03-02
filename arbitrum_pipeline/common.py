import os
import pandas as pd
import requests


def export_to_file(data: pd.DataFrame, group: str, filename: str) -> None:
    folder_name = "output_data/" + group

    csv_file_name = filename + ".csv"
    csv_file_path = os.path.join(folder_name, csv_file_name)
    data.to_csv(csv_file_path, index=False)
    print(f"Data exported to CSV file: {csv_file_name}")

    parquet_file_name = filename + ".parquet"
    parquet_file_path = os.path.join(folder_name, parquet_file_name)
    data.to_parquet(parquet_file_path, index=False)
    print(f"Data exported to Parquet file: {parquet_file_name}")


def request_graphql(
    url: str, query: str, variables: dict = None, additional_headers: dict = None
):
    headers = {
        "Content-Type": "application/json",
    }

    if additional_headers is not None:
        headers.update(additional_headers)

    payload = {"query": query}
    if variables is not None:
        payload["variables"] = variables

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("data", {})
