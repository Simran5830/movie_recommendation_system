from flask import Flask, request, render_template

import pickle
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

import requests

TMDB_API_KEY = 'bf575d5ad0d91975ac9e6b574e58153c'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

app=Flask(__name__)

# Load the data and model
with open('movie_list.pkl', 'rb') as f:
    data = pickle.load(f)
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

df=data.title.tolist()
# df_html = df.to_html(classes='table table-striped')

def get_movie_poster(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None


@app.route('/')
def home():
    return render_template('index.html', df_html=df);

@app.route('/', methods=['GET', 'POST'])
def recommend():
    poster_url = None
    poster=[]
    if request.method=='POST':
        result=[]
        movie=request.form.get('movie_val')
        index = data[data['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
        for i in distances[1:7]:
            result.append(data.iloc[i[0]].title)
            movie_id = data.iloc[i[0]].id
            poster_url= get_movie_poster(movie_id)
            poster.append(poster_url)
        return render_template('index.html', result=result, poster_url=poster)

if __name__=='__main__':
    app.run(debug=True)