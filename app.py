import streamlit as st
import pickle
import pandas as pd
import requests


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/ {}?api_key=9d3acac68e3150cd650b9ec4268c0058".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']
def recommend(movie):
    mov_index = movies[movies['title'] == movie].index[0]
    distances = similarity[mov_index]
    mov_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_poster = []
    for i in mov_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movies.iloc[i[0]].id))
    return recommended_movies, recommended_poster


st.title('Movie Recommeder System')

selected_movie = st.selectbox(
    'Enter the Movie Name',
    movies['title'].values)

if st.button('Recommend'):
    name,poster = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])