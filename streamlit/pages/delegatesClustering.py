import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def get_clustered_delegates_total():
    return pd.read_csv("../analytics/data/clustered_delegates_total.csv")


@st.cache_data
def get_pivot_votes():
    return pd.read_csv("../analytics/data/pivot_votes.csv")


@st.cache_data
def get_clustered_pca_delegates():
    return pd.read_csv("../analytics/data/clustered_pca_delegates.csv")


st.markdown("# Delegate clustering")

st.markdown("## Summary")

st.markdown(
    """
    - Conducted KMode clustering for Arbitrum Delegates based on their voting behavior
    - Idenfified common pattern for each cluster. In conclusion, delegating to cluster 3 Delegates is recommended.
"""
)

st.markdown("### Methodology")

st.markdown("#### Used data")
st.markdown(
    """
           Delegates: Delegators that are registered on Karma(1,421 Delegates)
           
           Voting: Snapshot voting data. filter by voting for proposals that have three standard choices, "For", "Agains" and "Abstain"(126 proposals and 21,140 votes by Delegates) 
"""
)

st.markdown("#### Pivot table(Delegates wallet addess X Voting choice)")
st.markdown("None represents 'No Vote'")

pivot_votes = get_pivot_votes()
pivot_votes.rename(columns={"publicAddress": "delegates address"}, inplace=True)

st.dataframe(pivot_votes, height=300)


st.markdown("#### Run KMode Clustering")
st.markdown(
    "[K-Mode clustering](https://pypi.org/project/kmodes/) is similart to k-means clustering, but more suitable for categorical data"
)

st.markdown(
    "#### Visualize clustering result by decreasing to two dimensions by PCA(Principal component analysis)"
)
clustered_pca_delegates = get_clustered_pca_delegates()

fig = px.scatter(
    clustered_pca_delegates,
    x=clustered_pca_delegates["feature1"],
    y=clustered_pca_delegates["feature2"],
    color=clustered_pca_delegates["cluster"],
    hover_name="publicAddress",
    title="Clustered Delegates",
)
st.plotly_chart(fig)

st.markdown("#### Interpret characteristics of cluster")
clustered_delegates_total = get_clustered_delegates_total()
clustered_delegates_total.fillna("")
clustered_delegates_total = clustered_delegates_total[
    [
        "publicAddress",
        "ensName",
        "cluster",
        "totalForVotes",
        "totalAgainstVotes",
        "totalAbstainVotes",
        "totalNoVotes",
    ]
]

fig = px.box(clustered_delegates_total, x="cluster", y="totalForVotes")
st.plotly_chart(fig)

fig = px.box(clustered_delegates_total, x="cluster", y="totalAgainstVotes")
st.plotly_chart(fig)

fig = px.box(clustered_delegates_total, x="cluster", y="totalAbstainVotes")
st.plotly_chart(fig)

fig = px.box(clustered_delegates_total, x="cluster", y="totalNoVotes")
st.plotly_chart(fig)

average_by_cluster = (
    clustered_delegates_total.groupby("cluster")[
        ["totalForVotes", "totalAgainstVotes", "totalAbstainVotes", "totalNoVotes"]
    ].mean()
    # .apply(lambda x: x / 144)
    # .applymap("{:.2%}".format)
)
average_by_cluster["total"] = average_by_cluster.sum(axis=1)
columns_to_divide = [
    "totalForVotes",
    "totalAgainstVotes",
    "totalAbstainVotes",
    "totalNoVotes",
]
average_by_cluster[columns_to_divide] = (
    average_by_cluster[columns_to_divide].div(average_by_cluster["total"], axis=0) * 100
).applymap("{:.2f}%".format)
average_by_cluster = average_by_cluster.drop(columns=["total"])

st.dataframe(average_by_cluster)

st.markdown(
    """
            Here we can see characteristics of the cluster.
            
            Cluster 0: rarely participates in voting
            
            Cluster 1: Voting for around half of the proposals much more "For" votes than "Against"
            
            Cluster 2: rarely participates in voting
            
            Cluster 3: voting most actively. voting "Agaist" as much as "For"
"""
)


st.markdown("#### Delegates list by cluster")
cluster_options = [0, 1, 2, 3]
selected_cluster = st.selectbox(
    "Select a cluster number:", cluster_options, index=list(cluster_options).index(3)
)

filtered_clustered_delegates_total = clustered_delegates_total[
    clustered_delegates_total["cluster"] == selected_cluster
]


st.dataframe(filtered_clustered_delegates_total, height=400)
