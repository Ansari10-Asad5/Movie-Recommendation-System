import streamlit as st
import pickle
import pandas as pd
import requests


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

print(movies)
class Details:
    def __init__(self,movie_id):
        response = requests.get("https://api.themoviedb.org/3/movie/ {}?api_key=9d3acac68e3150cd650b9ec4268c0058".format(movie_id))
        response1 = requests.get("https://api.themoviedb.org/3/movie/{}/credits?api_key=9d3acac68e3150cd650b9ec4268c0058&language=en-US".format(movie_id))
        data = response.json()
        data1 = response1.json()
        self.genre =", ".join([i['name'] for i in data['genres']])
        self.poster = "https://image.tmdb.org/t/p/original/" + data['poster_path']
        self.overview = data['overview']
        self.runtime = str(data['runtime'])
        cast_profile = []
        cast_name = []
        for i in range(3):
            cast_profile.append("https://image.tmdb.org/t/p/original" + data1['cast'][i]['profile_path'])
            cast_name.append(data1['cast'][i]['name'])

        self.cast_name = cast_name
        self.cast_profile = cast_profile
        for i in range(50):
            if data1['crew'][i]['job'] == 'Director':
                director = data1['crew'][i]['name']
                break
            else:
                director = ' '
                continue
        self.director = director

def recommend(movie):
    mov_index = movies[movies['title'] == movie].index[0]
    distances = similarity[mov_index]
    mov_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_poster = []
    Movie_genre = []
    overview = []
    runtime = []
    c_name = []
    c_profile = []
    directors = []
    for i in mov_list:
        movie_id = Details(movies.iloc[i[0]].id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_poster.append(movie_id.poster)
        Movie_genre.append(movie_id.genre)
        overview.append(movie_id.overview)
        runtime.append(movie_id.runtime)
        c_name.append(movie_id.cast_name)
        c_profile.append(movie_id.cast_profile)
        directors.append(movie_id.director)
    return recommended_movies, recommended_poster,Movie_genre,overview,runtime,c_name,c_profile,directors


st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Enter the Movie Name',
    movies['title'].values)
mov_index = movies[movies['title']==selected_movie].index[0]
movie_id = Details(movies.iloc[mov_index]['id'])
st.header(selected_movie)
st.image(movie_id.poster,width=200)
st.subheader('Cast')
st.image(movie_id.cast_profile, width=100, caption=movie_id.cast_name)
st.text('Director: '+movie_id.director)
st.text('Genre: '+movie_id.genre)
st.text('Overview: '+movie_id.overview)
st.text('Runtime: '+movie_id.runtime + ' min')


if st.button('Recommend'):
    name,poster,genre,Overview,runtime,cn,cp,d = recommend(selected_movie)
    # Overview = Mov_details(selected_movie)
    tab1, tab2, tab3, tab4, tab5= st.tabs([name[0],name[1],name[2],name[3],name[4]])

    with tab1:
        st.header(name[0])
        st.image(poster[0], width=200)
        st.subheader('Cast')
        st.image(cp[0], width=100, caption=cn[0])
        st.text('Director: '+d[0])
        st.text('Genre: '+genre[0])
        st.text('Overview: '+Overview[0])
        st.text('Runtime: '+runtime[0] + ' min')

    with tab2:
        st.header(name[1])
        st.image(poster[1], width=200)
        st.subheader('Cast')
        st.image(cp[1], width=100, caption=cn[1])
        st.text('Director: ' + d[1])
        st.text('Genre: '+genre[1])
        st.text('Overview: ' + Overview[1])
        st.text('Runtime: ' + runtime[1]+ ' min')

    with tab3:
       st.header(name[2])
       st.image(poster[2], width=200)
       st.subheader('Cast')
       st.image(cp[2], width=100, caption=cn[2])
       st.text('Director: ' + d[2])
       st.text('Genre: ' + genre[2])
       st.text('Overview: ' + Overview[2])
       st.text('Runtime: ' + runtime[2]+ ' min')
    with tab4:
       st.header(name[3])
       st.image(poster[3], width=200)
       st.subheader('Cast')
       st.image(cp[3], width=100, caption=cn[3])
       st.text('Director: ' + d[3])
       st.text('Genre: ' + genre[3])
       st.text('Overview: ' + Overview[3])
       st.text('Runtime: ' + runtime[3]+ ' min')

    with tab5:
       st.header(name[4])
       st.image(poster[4], width=200)
       st.subheader('Cast')
       st.image(cp[4], width=100, caption=cn[4])
       st.text('Director: ' + d[4])
       st.text('Genre: ' + genre[4])
       st.text('Overview: ' + Overview[4])
       st.text('Runtime: ' + runtime[4]+ ' min')



