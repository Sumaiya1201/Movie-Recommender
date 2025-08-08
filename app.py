import streamlit as st
import pickle
import pandas as pd
import gdown
import os

# Google Drive file ID for similarity.pkl
SIMILARITY_ID = "1JrWfYIAkCSOMM8L_N7OoNAyOc4PYfigM"

# Function to download file from Google Drive if not present
def download_file(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Download similarity.pkl from Google Drive
download_file(SIMILARITY_ID, "similarity.pkl")

# Load local movie_dict.pkl (already in repo)
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Which movie do you want to watch?',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)
