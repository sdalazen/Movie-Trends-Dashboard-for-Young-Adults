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
