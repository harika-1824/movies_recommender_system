import streamlit as st
import pickle
import requests

movies=pickle.load(open('movies_list.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path
def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distances=sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)
    recommended_movie_names=[]
    recommended_movie_posters=[]
   #We want to get 5 movies
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names,recommended_movie_posters
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

