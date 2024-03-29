from datetime import datetime
import re

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
    export_to_file(df, group, "raw_proposals")

    return Output(
        df,
        metadata={
            "Number of records": len(df),
        },
    )


@asset(group_name=group)
def preprocessed_snapshot_proposals(
    context: AssetExecutionContext, snapshot_proposals: pd.DataFrame
) -> Output[pd.DataFrame]:
    df = snapshot_proposals
    df["forum_topic_id"] = df["discussion"].apply(extract_forum_topic_id)
    # Convert forum_topic_id column to integers, handling NaN values(convert to -1) if necessary
    df["forum_topic_id"] = df["forum_topic_id"].fillna(-1).astype(int)

    df["duration"] = df["end"] - df["start"]
    df["created_date"] = pd.to_datetime(df["created"], unit="s", utc=True)

    # Get the choice with the highest score
    df["highest_score_index"] = df["scores"].apply(lambda x: x.index(max(x)))
    df["selected_choice"] = df.apply(
        lambda row: (
            row["choices"][row["highest_score_index"]]
            if len(row["choices"]) > row["highest_score_index"]
            else None
        ),
        axis=1,
    )

    context.log.info(df["selected_choice"].head())

    export_to_file(df, group, "cleaned_proposals")
    return Output(
        df,
        metadata={
            "Number of records": len(df),
        },
    )


def extract_forum_topic_id(url):
    # Regular expression to match the Forum ID in the URL
    pattern = r"/(\d{5})/?"
    match = re.search(pattern, url)
    return int(match.group(1)) if match else None


@asset(group_name=group)
def snapshot_votes(
    context: AssetExecutionContext, snapshot_proposals: pd.DataFrame
) -> Output[list]:
    created = 1
    all_data = []

    proposal_ids = snapshot_proposals["id"].to_list()

    context.log.info(proposal_ids)
    for proposal_id in proposal_ids:
        created = 1
        while True:
            # skip parameter has limitation we can fetch only up to 5000 records.
            # So, using created parameter and increment them to fetch all records.
            variables = {
                "proposal_id": proposal_id,
                "created": created,
            }

            context.log.info(
                f"Fetching data for proposal_id: {proposal_id}, created_at: {created}"
            )

            response_data = request_graphql(snapshot_base_url, votes_query, variables)

            votes_data = response_data.get("votes", [])

            if not votes_data:
                context.log.info("No more records to fetch.")
                break
            df = pd.DataFrame(votes_data)
            df["proposal_id"] = proposal_id
            # convert to str to avoid error
            df["choice"] = df["choice"].apply(lambda x: str(x))

            all_data.append(df)

            last_created = votes_data[-1].get("created")
            if last_created:
                created = last_created
            else:
                break

    print(df["choice"].unique())

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        context.log.info(final_df.head())
        export_to_file(final_df, group, "votes")
    else:
        context.log.info("No data was fetched.")

    return Output(
        all_data,
        metadata={
            # TODO: fix this
            "Number of records": len(all_data),
        },
    )


proposal_query = """
{
  proposals(
    first: 1000
    skip: 0
    where: { space_in: ["arbitrumfoundation.eth"] }
    orderBy: "created"
    orderDirection: asc
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
query Votes($proposal_id: String!, $created: Int!) {
  votes(
    first: 1000
    where: {
      proposal: $proposal_id
      created_gt: $created
    }
    orderBy: "created"
    orderDirection: asc
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
