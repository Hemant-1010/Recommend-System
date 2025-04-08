import streamlit as st
import pickle
import requests
import pandas as pd

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)





# -----------------------------
# TMDB Poster Fetch Function
# -----------------------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=62779883614a0011509171f0589efa22&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except:
        return "https://via.placeholder.com/300x450?text=Error"

# -----------------------------
# Cache Loading Data
# -----------------------------
@st.cache_data
def load_data():
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    return movies, similarity

movies, similarity = load_data()

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in dataset.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_titles = []
    recommended_posters = []

    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]].id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters

# -----------------------------
# UI - Movie Selector
# -----------------------------
movie_titles = movies['title'].values
selected_movie = st.selectbox("🔎 Search for a movie to get recommendations:", sorted(movie_titles))

# -----------------------------
# Recommend Button
# -----------------------------
if st.button("🎥 Show Recommendations"):
    recommended_titles, recommended_posters = recommend(selected_movie)

    if recommended_titles:
        st.subheader("📌 Top 5 Similar Movies:")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(recommended_posters[i])
                st.markdown(f"**{recommended_titles[i]}**")


  
