import pandas as pd
from arbitrum_pipeline.common import export_to_file, request_graphql
from dagster import asset, Output, AssetExecutionContext
from dotenv import load_dotenv
import os

load_dotenv()

TALLY_API_KEY = os.getenv("TALLY_API_KEY")

tally_base_url = "https://api.tally.xyz/query"
group = "tally"


@asset(group_name=group)
def tally_proposals(context: AssetExecutionContext) -> Output[pd.DataFrame]:
    additional_headers = {"Api-key": TALLY_API_KEY}
    response_data = request_graphql(
        tally_base_url, proposal_query, None, additional_headers
    )

    df = pd.DataFrame(response_data.get("governance", {}).get("proposals", []))
    context.log.info(df.head())
    export_to_file(df, group, "proposals")

    return Output(
        df,
        metadata={
            "Number of records": len(df),
        },
    )


proposal_query = """
{
  governance(id: "eip155:42161:0xf07DeD9dC292157749B6Fd268E37DF6EA38395B9") {
    id
    chainId
    organization {
      id
      slug
    }
    proposals {
      id
      title
      description
      eta
      proposer {
        id
      }
    }
    active
    name
  }
}
"""
