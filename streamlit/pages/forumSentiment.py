import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def get_sentiment_by_proposal():
    return pd.read_csv("analytics/data/sentiment_by_proposal.csv")


st.markdown("# Sentiment Analysis on Forum posts and Effect on Voting behavior")


st.markdown("## Summary")
st.markdown(
    """
    - Combined [Snapshot](https://snapshot.org/#/arbitrumfoundation.eth) proposals and corresponding Forum posts, then conducted sentiment analysis by [Textblob](https://textblob.readthedocs.io/en/dev/index.html#)
    - Polarity score of passed proposals is higher than others
    - The more positive and objective information in the Forum post, the more votes in proposal
            """
)

st.markdown("## Sentiment(Polarity&Subjectivity) for proposals")
st.markdown(
    "I've ran sentiment analysis for each post on Forum and group by associated Snapshot proposals."
)
sentiment_by_proposal = get_sentiment_by_proposal()

sentiment_by_proposal["Forum_topic_URL"] = sentiment_by_proposal[
    "forum_topic_id"
].apply(lambda x: f"https://forum.arbitrum.foundation/t/{x}")
sentiment_by_proposal = sentiment_by_proposal.drop(
    columns=["id_proposal", "scores_total", "forum_topic_id"]
)

st.write(
    "TextBlob is a well-known python library for Natural Language Processing (NLP)"
)

st.dataframe(sentiment_by_proposal)
st.markdown(
    "- **Polarity scores** are range from -1 to 1, where -1 indicates a very negative sentiment, 0 indicates a neutral sentiment, and 1 indicates a very positive sentiment."
)
st.markdown(
    "- **Subjectivity scores** are range from 0 to 1, where 0 indicates a very objective text, and 1 indicates a very subjective text."
)
st.markdown(
    """
    [Sentiment Analysis using TextBlob](https://towardsdatascience.com/my-absolute-go-to-for-sentiment-analysis-textblob-3ac3a11d524)
"""
)

st.markdown("## Correlation between sentiment and voting result")

sentiment_by_proposal = sentiment_by_proposal[
    sentiment_by_proposal["selected_choice"].isin(["For", "Against", "Abstain"])
]

figPol = px.box(
    sentiment_by_proposal,
    x="selected_choice",
    y="polarity",
    title="Average Polarity score by selected choice",
)
st.plotly_chart(figPol)

st.write(
    "Polarity score of proposals the final selected choice is 'For'(= Passed proposal) is higher than Against or Abstain proposals, and there is a statistically significant difference(p=0.00017)"
)

figSub = px.box(
    sentiment_by_proposal,
    x="selected_choice",
    y="subjectivity",
    title="Average Subjectivity score by selected choice",
)
st.plotly_chart(figSub)

st.write(
    "No clear statistical difference regarding Subjectivity score by selected choice"
)


figVoteAndPol = px.scatter(
    sentiment_by_proposal,
    x="polarity",
    y="votes",
    hover_name="title_proposal",
    trendline="ols",
    trendline_color_override="darkblue",
    title="Total Votes by proposal's polarity",
)
st.plotly_chart(figVoteAndPol)

st.write(
    "We can see a weak correlation between number of votes and polarity score.(r=0.22)"
)

figVoteAndSub = px.scatter(
    sentiment_by_proposal,
    x="subjectivity",
    y="votes",
    hover_name="title_proposal",
    trendline="ols",
    trendline_color_override="darkblue",
    title="Total votes by proposal's subjectivity",
)
st.plotly_chart(figVoteAndSub)
st.write(
    "A weak negative correlation between number of votes and subjectivity score(r=0.3), which means more votes if there are factual information than personal opinion(Forum posts are objective)."
)


st.markdown("#### Future work")
st.markdown(
    """
            At the moment, it's hard to do sentiment analysis per voter basis because we can't tie Forum posters with snapshot voters.
            https://github.com/OpenDataforWeb3/DataGrantsforARB/issues/6#issuecomment-1937396931
            Once it's available, we can make use of this methodology for more advanced analysis.
            """
)

st.markdown("#### Appendix")
st.write(
    "Jupyter notebook file and data is available at https://github.com/junta/arbitrum-data-pipeline/blob/main/analytics"
)
