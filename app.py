import streamlit as st
import os
import gdown
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()

    #error handling for missing posters
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    indices = movies[movies['title'] == movie].index  # <-- ADDED: check if movie exists safely
    if len(indices) == 0:
        st.error("Movie '" + movie + "' not found!")  # <-- ADDED: error message if movie not found
        return [], []

    movie_index = indices[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

file_path = "similarity.pkl"

if not os.path.exists(file_path):
    st.write("Downloading similarity.pkl from Google Drive...")
    url = "https://drive.google.com/uc?id=1hg09gG6UTywp25-RacyIJZztMX5MsF_f"
    try:
        gdown.download(url, file_path, quiet=False)
    except Exception as e:
        st.error("Failed to download similarity.pkl: " + str(e))
        st.stop()  # stop the app if file not available

similarity = pickle.load(open(file_path, 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Select a movie to get recommendations:',
movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    if names == []:
        st.warning("No recommendations found.")  # <-- ADDED: handle empty recommendation case gracefully
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])

