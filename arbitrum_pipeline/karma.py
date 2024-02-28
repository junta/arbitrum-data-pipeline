from time import sleep
import requests
import pandas as pd
from arbitrum_pipeline.common import export_to_file, request_graphql
from dagster import asset, Output, AssetExecutionContext


karma_base_url = "https://api.karmahq.xyz/api/dao"
group = "karma"


@asset(group_name=group)
def delegates(context: AssetExecutionContext) -> Output[pd.DataFrame]:
    url = karma_base_url + "/delegates?name=arbitrum&pageSize=1000&period=lifetime"

    delegates = []
    offset = 0

    while True:
        params = {"offset": offset}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        page_delegates = data.get("data", {}).get("delegates", [])
        print("current offset: ", offset)

        if not page_delegates:
            break

        delegates.extend(page_delegates)
        offset += 1
        sleep(1)

    df = pd.DataFrame(delegates)
    context.log.info(df.head())
    # remove to avoid error for now
    df = df.drop(columns=["delegatePitch"])

    export_to_file(df, group, "delegates")

    return Output(
        df,
        metadata={
            "Number of records": len(df),
        },
    )
