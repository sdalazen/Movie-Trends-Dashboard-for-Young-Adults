import streamlit as st
import pandas as pd
import numpy as np

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

# Top-rated movies
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
