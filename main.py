import pickle
import streamlit as st
import requests
import pandas as pd

# --- Fetch poster from TMDB ---
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7cfc2a3f18309bf8b5a1b2e2aefda994&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Image"

# --- Recommend movies ---


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# --- Load Data ---
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')

# Load from correct file
movies_dict = pickle.load(open('PycharmProjects/helloWorld/Streamlit Dashboard/similar.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('PycharmProjects/helloWorld/Streamlit Dashboard/similar.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# --- Recommendation Display ---
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"**{names[i]}**")
