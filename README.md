# Analyzing Horror Trends with TMDB Data

This project was completed as part of the interview process with the Data School. The goal of this project was to choose an interesting dataset and create a Tableau dashboard the effectively communicates your data in a storytelling format. For my project, I chose to analyze the popularity and profitability of horror movies.

Using TMDB (The Movie Database) data, I answered the following main questions:
- Why I am seeing more Horror movies? Are they becoming more popular?
- Why are horror movies so profitable?
- Are horror movies more profitable during October?

## Introduction

The topic of this data project stemmed from a question that I had been wanting to answer myself. I recently got an AMC Stubs membership because I’ve been watching movies in theatres with my significant other. Before a movie starts, other movie trailers will play for 20-25 minutes. This is actually one of my favorite things about going to the movie theaters, which is an experience that doesn’t happen at home. 

I tend to get scared very easily, so when trailers for new horror films come out, I shut my ears and close my eyes, waiting for it to pass. I remember while we were watching the trailers, I kept thinking “again?” as another creepy film trailer showed on the big screen. I knew I wasn’t the only one who thought that horror films were on the rise when the search, “is horror becoming more popular?” resulted in multiple reddit posts. Despite me being a scaredy cat, I wanted to answer why horror was becoming more popular, using data that I queried from the TMDB API. 

## Data Collection 

I primarily used TMDB because it's a free API that provides the budget and revenue of each movie, unlike the IMDB datasets. Using a python script (tmdb_clean.py), I queried for all movies between 2000 and 2025 with a vote count >= 100. Having a vote count >= 100 means that at least 100 people have to rate the movie on TMDB. A vote count of 100 or greater was added due to API limitations on the number of movies that can be queried. For each year, the API will only return the top 10,000 movies based on popularity. Since most years have more than 10,000 movies released, I set a limitation on the number of votes to make the data more interpretable. Data cleaning was fairly simple, since most of the API data is clean. Once the data was stored, I outputted the data into a csv called tmdb.csv.

## Data Visualization:

My Tableau dashboard can be found here: https://public.tableau.com/app/profile/serena.lee3512/viz/25YearsofHorror/Dashboard5


