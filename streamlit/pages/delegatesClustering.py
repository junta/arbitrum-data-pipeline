import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def get_clustered_delegates_total():
    return pd.read_csv("analytics/data/clustered_delegates_total.csv")


@st.cache_data
def get_pivot_votes():
    return pd.read_csv("analytics/data/pivot_votes.csv")


@st.cache_data
def get_clustered_pca_delegates():
    return pd.read_csv("analytics/data/clustered_pca_delegates.csv")


st.markdown("# Delegates Clustering by Voting behavior")

st.markdown("## Summary")

st.markdown(
    """
    - Conducted K-Mode clustering for Arbitrum Delegates based on their voting behavior
    - Idenfified common pattern for each cluster. In conclusion, Delegates in Cluster3 have partcipated in voting most actively. (There is a list below) 
    - Although Karma provides high quality information, choosing delegates remains a challenging task. Clustering can significantly contribute to comprehending delegate behavior and offering valuable insights to users.
"""
)

st.markdown("### Methodology")

st.markdown("#### Data")
st.markdown(
    """
           **Delegates:** Delegates that are registered on [Karma](https://arbitrum.karmahq.xyz/)(1,421 Delegates)
           
           **Voting:** [Snapshot](https://snapshot.org/#/arbitrumfoundation.eth) voting data. filter by voting for proposals that have three standard choices, "For", "Agains" and "Abstain"(126 proposals and 21,140 votes by Delegates) 
"""
)

st.markdown("#### Pivot table(Voting behavior by Delegates)")
st.markdown("*None represents 'No Vote'")

pivot_votes = get_pivot_votes()
pivot_votes.rename(columns={"publicAddress": "delegates address"}, inplace=True)

st.dataframe(pivot_votes, height=300)


st.markdown("#### Run K-Mode Clustering")
st.markdown(
    "I've selected [K-Mode clustering](https://pypi.org/project/kmodes/) as clustering algorithm, and categorized delegates to 4 clusters. K-Mode clustering is similar to k-means clustering, but more suitable for categorical data"
)

clustered_pca_delegates = get_clustered_pca_delegates()

st.markdown(
    "#### Visualize clustering result by decreasing to two dimensions by PCA(Principal component analysis)"
)


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

fig = px.box(
    clustered_delegates_total,
    x="cluster",
    y="totalForVotes",
    title="'For' votes by delegates cluster",
)
st.plotly_chart(fig)

fig = px.box(
    clustered_delegates_total,
    x="cluster",
    y="totalAgainstVotes",
    title="'Against' votes by delegates cluster",
)
st.plotly_chart(fig)

fig = px.box(
    clustered_delegates_total,
    x="cluster",
    y="totalAbstainVotes",
    title="'Abstain' votes by delegates cluster",
)
st.plotly_chart(fig)

fig = px.box(
    clustered_delegates_total,
    x="cluster",
    y="totalNoVotes",
    title="No votes by delegates cluster",
)
st.plotly_chart(fig)

average_by_cluster = clustered_delegates_total.groupby("cluster")[
    ["totalForVotes", "totalAgainstVotes", "totalAbstainVotes", "totalNoVotes"]
].mean()

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

average_by_cluster["NumberOfDelegates"] = [263, 34, 441, 74]
average_by_cluster = average_by_cluster[
    [
        "NumberOfDelegates",
        "totalForVotes",
        "totalAgainstVotes",
        "totalAbstainVotes",
        "totalNoVotes",
    ]
]

st.dataframe(average_by_cluster)

st.markdown(
    """
            Here, we can see characteristics of each cluster.
            
            **Cluster 0:** Rarely participates in voting
            
            **Cluster 1:** Voting for around half of the proposals. Much more "For" votes than "Against"
            
            **Cluster 2:** Voting more than cluster 0, but still less
            
            **Cluster 3:** Voting most actively(Vote for more than 90% of proposals). Voting "Agaist" as much as "For"
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

st.markdown("#### Appendix")
st.write(
    "Jupyter notebook file and data is available at https://github.com/junta/arbitrum-data-pipeline/blob/main/analytics"
)
