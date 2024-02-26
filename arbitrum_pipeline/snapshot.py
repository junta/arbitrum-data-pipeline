from time import sleep
import requests
import pandas as pd
from arbitrum_pipeline.common import export_to_file, request_graphql
from dagster import asset
import os

snapshot_base_url = "https://hub.snapshot.org/graphql"
group = "snapshot"


@asset
def fetch_proposals() -> pd.DataFrame:
    response_data = request_graphql(snapshot_base_url, proposal_query)

    df = pd.DataFrame(response_data.get("proposals", []))
    print(df.head())
    export_to_file(df, group, "proposals")
    return df


proposal_query = """
{
  proposals(
    first: 1000
    skip: 0
    where: { space_in: ["arbitrumfoundation.eth"] }
    orderBy: "created"
    orderDirection: desc
  ) {
    id
    title
    body
    choices
    start
    end
    snapshot
    state
    author
    scores
    votes
    flagged
  }
}
"""
