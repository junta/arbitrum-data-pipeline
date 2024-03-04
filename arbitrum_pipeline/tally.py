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

    df_start = pd.json_normalize(df["start"])
    df_start = df_start.rename(columns={"timestamp": "start_timestamp"})
    df = df.drop("start", axis=1)
    df_end = pd.json_normalize(df["end"])
    df_end = df_end.rename(columns={"timestamp": "end_timestamp"})
    df = df.drop("end", axis=1)

    normalized_df = pd.concat([df, df_start, df_end], axis=1)
    export_to_file(normalized_df, group, "proposals")

    return Output(
        normalized_df,
        metadata={
            "Number of records": len(normalized_df),
        },
    )


proposal_query = """
{
  governance(id: "eip155:42161:0xf07DeD9dC292157749B6Fd268E37DF6EA38395B9") {
    id
    chainId
    active
    name
    organization {
      id
      slug
    }
    proposals {
      id
      title
      description
      start {
        ... on Block {
          timestamp
        }
      }
      end {
        ... on Block {
          timestamp
        }
      }
      eta
      executable {
        callDatas
        signatures
        targets
        values
      }
      voteStats {
        support
        weight
        votes
        percent
      }
      proposer {
        id
        name
        address
        ens
        bio
      }
    }    
  }
}
"""
