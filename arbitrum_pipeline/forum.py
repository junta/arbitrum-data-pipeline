from time import sleep
import requests
import pandas as pd
from arbitrum_pipeline.common import export_to_file
from dagster import asset, Output


forum_base_url = "https://forum.arbitrum.foundation"
group = "forum"


@asset(group_name="forum")
def forum_topics() -> Output[pd.DataFrame]:
    url = forum_base_url + "/latest.json"
    topics = []
    page = 1

    while True:
        params = {"page": page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        page_topics = data.get("topic_list", {}).get("topics", [])
        print("current page: ", page)

        if not page_topics:
            break

        topics.extend(page_topics)
        page += 1
        sleep(1)

    df = pd.DataFrame(topics)
    # tags_descriptions is not used, so remove it to avoid error when exporting to Parquet
    df = df.drop(columns=["tags_descriptions"])
    export_to_file(df, group, "topics")

    return Output(
        df,
        metadata={
            "Number of records": len(df),
        },
    )


@asset(group_name="forum")
def forum_categories() -> Output[pd.DataFrame]:
    url = forum_base_url + "/categories.json"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    categories = data.get("category_list", {}).get("categories", [])

    df = pd.DataFrame(categories)
    export_to_file(df, group, "categories")

    return Output(
        df,
        metadata={
            "Number of records": len(df),
        },
    )


@asset(group_name="forum")
def forum_users() -> pd.DataFrame:
    url = forum_base_url + "/directory_items.json"
    users = []
    page = 1

    while True:
        params = {"period": "all", "page": page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        page_users = data.get("directory_items", [])
        print("current page: ", page)

        if not page_users:
            break

        users.extend(page_users)
        page += 1
        sleep(1)

    df = pd.DataFrame(users)

    # extract to another asset
    user_detail_df = pd.json_normalize(df["user"])
    user_detail_df = user_detail_df.rename(columns={"id": "user_id"})

    # drop original user object
    df = df.drop("user", axis=1)

    normalized_df = pd.concat([df, user_detail_df], axis=1)
    export_to_file(normalized_df, group, "users")
    return df


@asset(group_name="forum")
def forum_posts() -> pd.DataFrame:
    url = forum_base_url + "/posts.json"
    posts = []

    def fetch_posts(before_id=None):
        params = {"before": before_id} if before_id else {}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get("latest_posts", [])
        except requests.HTTPError as e:
            print(f"Request failed: {e}")
            return []

    # Initial fetch
    page_posts = fetch_posts()
    posts.extend(page_posts)
    if page_posts:
        before_id = page_posts[-1]["id"]
        print("last post id: ", before_id)

    # Fetch remaining pages
    while page_posts and before_id > 1:
        page_posts = fetch_posts(before_id=before_id)
        if not page_posts:
            break
        posts.extend(page_posts)
        before_id = page_posts[-1]["id"]
        print("last post id: ", before_id)
        sleep(1)

    df = pd.DataFrame(posts)
    export_to_file(df, group, "posts")
    return df
