import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def get_sentiment_by_proposal():
    return pd.read_csv("../analytics/data/sentiment_by_proposal.csv")


st.markdown("# Sentiment Analysis on Forum post and voting behavior")

st.markdown("## Summary")
st.markdown(
    """
    - Combined Snapshot proposals and corresponding Forum posts, then conducted sentiment analysis by [Textblob](https://textblob.readthedocs.io/en/dev/index.html#)
    - Polarity score is higher for passed proposals(final selected choice is "For") than others
            """
)

st.markdown("## Sentiment(Polarity&Subjectivity) for proposals")
sentiment_by_proposal = get_sentiment_by_proposal()
sentiment_by_proposal = sentiment_by_proposal.drop(
    columns=["id_proposal", "scores_total"]
)
st.dataframe(sentiment_by_proposal)
st.write(
    "Polarity scores are range from -1 to 1, where -1 indicates a very negative sentiment, 0 indicates a neutral sentiment, and 1 indicates a very positive sentiment."
)
st.write(
    "Subjectivity scores are numerical values that range from 0 to 1, where 0 indicates a very objective text, and 1 indicates a very subjective text."
)

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
    "Polarity score of proposals that final selected choice is 'For' is higher than Against or Abstain proposals and clear statistical difference(p=0.00017)"
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


fig = px.scatter(
    sentiment_by_proposal,
    x="polarity",
    y="votes",
    hover_name="title_proposal",
    trendline="ols",
    trendline_color_override="darkblue",
    title="Total votes by proposal's polarity",
)
st.plotly_chart(fig)
