import tmdbsimple as tmdb
import pandas as pd
from tqdm import tqdm
import time
import requests


tmdb.API_KEY = '320e022133732be74202fef6c1ce2b6c'
tmdb.REQUESTS_SESSION = requests.Session()
tmdb.REQUESTS_TIMEOUT = (2, 5) 

'''
movies = pd.read_csv('./clean_data/Q2.csv')

movies['primaryTitle'] = movies['primaryTitle'].str.replace('Damned Gold', 'Damned Gold 2').replace('ı', 'i')

movie_names = movies['primaryTitle']


search = tmdb.Search()
ids = []
unsuccessful = []
for m in movie_names[:10]:
    response = search.movie(query=m)
    change = False
    for s in search.results:
        if s['original_title'] == m and change == False:
            change = True
            ids.append(s['id'])
            break
        if change == False and s['title'] == m:
            change = True
            ids.append(s['id'])
            break
    if change == False:
        print('name:', m, 'search:', search.results)
'''
years = list(range(2000, 2026))
#27 is horror genre
ids = []
for x in years:
    identity = tmdb.Discover()
    total_pages = identity.movie(language='en', primary_release_year=x, vote_count_gte=100)['total_pages']
    print(x, total_pages)
    if total_pages > 500:
        total_pages = 500
    for i in range(1,total_pages+1):
        response = identity.movie(language='en', primary_release_year=x, page=i, vote_count_gte=100)
        for m in response['results']:
            ids.append(m['id'])

rows = []
for m in ids:
    movie = tmdb.Movies(m)
    response = movie.info()
    rows.append({
        'id': response['id'],
        'budget': response['budget'],
        'imdb_id': response['imdb_id'],
        'genres': ', '.join([x['name'] for x in response['genres']]),
        'overview': response['overview'],
        'original_title': response['original_title'],
        'popularity': response['popularity'],
        'production_companies': ', '.join([x['name'] for x in response['production_companies']]),
        'production_countries': ', '.join([x['iso_3166_1'] for x in response['production_countries']]),
        'release_date': response['release_date'],
        'revenue': response['revenue'],
        'runtime': response['runtime'],
        'status': response['status'],
        'vote_average': response['vote_average'],
        'title': response['title'],
        'tagline': response['tagline'],
        'vote_count': response['vote_count']
    })

df = pd.DataFrame(rows)
print(len(df))
df.to_csv("clean_data/tmdb.csv")


