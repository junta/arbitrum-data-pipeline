import pandas as pd

cleaned_proposals = pd.read_parquet("output_data/snapshot/cleaned_proposals.parquet")
print(cleaned_proposals["forum_id"])

forum_topics = pd.read_parquet("output_data/forum/topics.parquet")

merged_df = pd.merge(cleaned_proposals, forum_topics, left_on="forum_id", right_on="id")
print(merged_df)


# df = pd.read_parquet("output_data/topics.parquet")
# print(df.head())

# df = pd.read_parquet("output_data/posts.parquet")
# print(df.head())
