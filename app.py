import streamlit as st
import pickle
import pandas as pd
import requests

s = requests.Session()


def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=ff908b9511e6589713db6bf7d3093231&language=en-US'.format(
        movie_id)
    data = s.get(url)
    data = data.json()
    try:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        full_path = None
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[0:30]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


def make_grid(cols, rows):
    grid = [0] * cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def show_recommendations(selected_movie):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    for i in range(0, 30, 3):
        recommended_movie_name_c1 = recommended_movie_names[i]
        recommended_movie_poster_c1 = recommended_movie_posters[i]
        recommended_movie_name_c2 = recommended_movie_names[i + 1]
        recommended_movie_poster_c2 = recommended_movie_posters[i + 1]
        recommended_movie_name_c3 = recommended_movie_names[i + 2]
        recommended_movie_poster_c3 = recommended_movie_posters[i + 2]

        grid_index = int(i / 3)
        my_grid[grid_index][0].write(recommended_movie_name_c1)
        try:
            my_grid[grid_index][0].image(recommended_movie_poster_c1)
        except:
            my_grid[grid_index][0].write("Poster unavailable")

        my_grid[grid_index][1].write(recommended_movie_name_c2)
        try:
            my_grid[grid_index][1].image(recommended_movie_poster_c2)
        except:
            my_grid[grid_index][0].write("Poster unavailable")

        my_grid[grid_index][2].write(recommended_movie_name_c3)
        try:
            my_grid[grid_index][2].image(recommended_movie_poster_c3)
        except:
            my_grid[grid_index][0].write("Poster unavailable")

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
movie_list = movies['title'].values

## font size of text of selectbox
str = 'Enter the name of the movie you want to search '
##
selected_movie = st.selectbox(
    str,
    movie_list
)

if st.button('Show Recommendation'):
    my_grid = make_grid(10, (3, 3, 3))
    show_recommendations(selected_movie)


hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

###############################
import pyttsx3
import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
if st.button('voice recommder'):
    st.write('Say movie name')
    try:

        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            #MyText = MyText.lower()

            st.write("Did you say ", MyText)
            SpeakText(MyText)
            flag =0
            #show_recommendations(MyText)
            subs = MyText
            res = list(filter(lambda x: subs in x, movie_list))

            if len(res) == 0:
                st.write("No movie avaiable for this search")
            else:
                for movie in movie_list:
                    if (movie == res[0]):
                        my_grid = make_grid(10, (3, 3, 3))
                        show_recommendations(movie)
                        flag = 1;
                        break;
                if (flag == 0):
                    st.write("Poster unavailable")


            #selected_movie2 = st.selectbox()

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")

##############
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/free-vector/elegant-business-background-with-lines-template_1361-2542.jpg?w=360");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()