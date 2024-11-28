import requests
import streamlit as st
import pickle
import pandas as pd


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4c6ac0f99d8d6331f56ae29a09a81e87&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # posters from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


# load the movies
movies_dictionary = pickle.load(open('movies_dictionary.pkl','rb'))
movies = pd.DataFrame(movies_dictionary)

# load the similarity matrix
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System')

selected_movie = st.selectbox(
    'Select the movie',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)
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