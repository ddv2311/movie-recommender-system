import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_posters(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=f3283d04d917d3f7aca36f5f700c9f0c&language=en-US'.format(movie_id)
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies = []
    recommend_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_posters(movie_id))
    
    return recommend_movies, recommend_movies_posters

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

option = st.selectbox(
    'Select a movie',
    movies_list
)

if st.button('Recommend'):
    names, posters = recommend(option)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)
