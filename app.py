import streamlit as st
import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv")
st.write(movies.columns)
movies['tagline'] = movies['overview']
movies['tagline'] = movies['tagline'].fillna('')

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags'].fillna('')).toarray()
similarity = cosine_similarity(vectors)

def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []
    for i in movie_list:
        recommendations.append(movies.iloc[i[0]].title)

    return recommendations
st.header("Movie Recommender System")
movie_list=movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown",movie_list,index=None)

if st.button("Show Recommendations"):
    if selected_movie is None:
        st.warning("Please select a movie first")
    else:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    c0,c1,c2,c3,c4=st.columns(5)
    with c0:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with c1:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with c2:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with c3:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with c4:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

