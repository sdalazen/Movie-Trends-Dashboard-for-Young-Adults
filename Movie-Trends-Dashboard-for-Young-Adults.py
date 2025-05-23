import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Movie Trends Dashboard for Young Adults (18–35)")

@st.cache_data
def load_data():
    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('movies.csv', encoding='ISO-8859-1')
    tags = pd.read_csv('tags.csv', encoding='ISO-8859-1')
    return ratings, movies, tags

ratings, movies, tags = load_data()

st.write("Ratings columns:", ratings.columns.tolist())
st.write("Movies columns:", movies.columns.tolist())
st.write("Tags columns:", tags.columns.tolist())

merged = ratings.merge(movies, on='movieId').merge(tags, on=['movieId', 'userId'], how='left')

st.subheader("Top Rated Movies")
top_movies = (
    merged.groupby('title')['rating']
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig_top_movies = px.bar(top_movies, x='rating', y='title', orientation='h', title='Top 10 Movies')
st.plotly_chart(fig_top_movies)

st.subheader("🎭 Most Common Genres")
genre_exploded = movies.copy()
genre_exploded['genres'] = genre_exploded['genres'].str.split('|')
genre_exploded = genre_exploded.explode('genres')
top_genres = genre_exploded['genres'].value_counts().reset_index()
top_genres.columns = ['Genre', 'Count']
fig_genres = px.pie(top_genres, values='Count', names='Genre', title='Genre Distribution')
st.plotly_chart(fig_genres)

st.subheader("Popular Tags")
tag_counts = tags['tag'].value_counts().head(20).reset_index()
tag_counts.columns = ['Tag', 'Count']
fig_tags = px.bar(tag_counts, x='Tag', y='Count', title='Top 20 Tags')
st.plotly_chart(fig_tags)

st.subheader("Why is this Data Suitable for Machine Learning?")
st.markdown("""
- Large volume of user interaction data (ratings, tags).
- Temporal patterns (timestamps).
- Rich categorical data (genres, tags).
- Opportunity to predict user preferences, recommend movies, and identify genre trends.
""")

st.sidebar.title("Design for 18–35 Age Group")
st.sidebar.markdown("""
- Minimalist layout with emojis for engagement.
- Interactive visuals (bar, pie charts).
- Quick insights without overwhelming detail.
- Trending content focus aligns with younger user interests.
""")

ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')
ratings_by_month = ratings.set_index('timestamp').resample('M')['rating'].mean().reset_index()
fig_time = px.line(ratings_by_month, x='timestamp', y='rating', title='Average Rating Over Time')
st.plotly_chart(fig_time)

top_by_count = merged['title'].value_counts().head(10).reset_index()
top_by_count.columns = ['title', 'count']
fig_count = px.bar(top_by_count, x='count', y='title', orientation='h', title='Top 10 Most Rated Movies')
st.plotly_chart(fig_count)