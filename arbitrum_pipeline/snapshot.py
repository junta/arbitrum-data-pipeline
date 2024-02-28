from time import sleep

import pandas as pd
from arbitrum_pipeline.common import export_to_file, request_graphql
from dagster import asset, Output, AssetExecutionContext


snapshot_base_url = "https://hub.snapshot.org/graphql"
group = "snapshot"


@asset(group_name=group)
def snapshot_proposals(context: AssetExecutionContext) -> Output[pd.DataFrame]:
    response_data = request_graphql(snapshot_base_url, proposal_query)

    df = pd.DataFrame(response_data.get("proposals", []))
    context.log.info(df.head())
    export_to_file(df, group, "proposals")

    return Output(
        df,
        metadata={
            "Number of records": len(df),
        },
    )


@asset(group_name=group)
def snapshot_votes(context: AssetExecutionContext) -> Output[pd.DataFrame]:
    response_data = request_graphql(snapshot_base_url, votes_query)

    df = pd.DataFrame(response_data.get("votes", []))
    context.log.info(df.head())
    export_to_file(df, group, "votes")

    return Output(
        df,
        metadata={
            "Number of records": len(df),
        },
    )


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
      discussion
      quorum
      privacy
      link
      app
      scores_by_strategy
      scores_state
      scores_total
      scores_updated
      strategies {
          name
          network
          params
      }
      type
      symbol
      network
      updated
      created
      ipfs
  }
}
"""

votes_query = """
query Votes {
  votes (
    first: 1000
    where: {
      proposal: "0x07a26cd6b78a41745aab04190f22e97fdf9432f564651d0c4da0f8d0827888a6"
    }
  ) {
    id
    voter
    created
    choice
    vp
    vp_by_strategy
    vp_state
    reason
    app
  }
}
"""
