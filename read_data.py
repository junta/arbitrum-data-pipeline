import pandas as pd

df = pd.read_parquet("output_data/topics.parquet")
print(df.head())

df = pd.read_parquet("output_data/posts.parquet")
print(df.head())
