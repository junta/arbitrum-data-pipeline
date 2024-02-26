from dagster import build_assets_job
from dagster.core.execution.execute_in_process_result import ExecuteInProcessResult
import pandas as pd

from your_asset_module import process_data

def test_process_data():
    # Build a job to run the asset
    job = build_assets_job("test_job", assets=[fetch_forum_topics])
    
    # Execute the job in process and capture the result
    result: ExecuteInProcessResult = job.execute_in_process()
    
    # Retrieve the output of the process_data asset
    output_df = result.output_for_node("process_data")
    
    # Define what the expected DataFrame should look like
    # expected_data = {'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]}
    # expected_df = pd.DataFrame(expected_data)
    
    # # Assert that the output DataFrame matches the expected DataFrame
    # pd.testing.assert_frame_equal(output_df, expected_df)