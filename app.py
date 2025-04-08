import streamlit as st
import pickle
import requests
import pandas as pd
import base64

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")




# Load and encode local image
def get_base64_of_bin_file(png_file):
    with open(png_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set background using CSS and base64
def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    css_code = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# Call it with your PNG file
set_png_as_page_bg("a.png")











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


  
