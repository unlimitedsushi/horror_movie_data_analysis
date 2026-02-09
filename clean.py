import duckdb

BASICS = "data/title.basics.tsv.gz"
CREW   = "data/title.crew.tsv.gz"
AKAS  = "data/title.akas.tsv.gz"
NAMES = "data/name.basics.tsv.gz"
RATINGS = "data/title.ratings.tsv.gz"

con = duckdb.connect()

#query 1: horror films vs. total films per decade

query1 = f"""
WITH titles_all AS (
    SELECT CASE
        WHEN startYear >= 1910 AND startYear < 1920 THEN '1910s'
        WHEN startYear >= 1920 AND startYear < 1930 THEN '1920s'
        WHEN startYear >= 1930 AND startYear < 1940 THEN '1930s'
        WHEN startYear >= 1940 AND startYear < 1950 THEN '1940s'
        WHEN startYear >= 1950 AND startYear < 1960 THEN '1950s'
        WHEN startYear >= 1960 AND startYear < 1970 THEN '1960s'
        WHEN startYear >= 1970 AND startYear < 1980 THEN '1970s'
        WHEN startYear >= 1980 AND startYear < 1990 THEN '1980s'
        WHEN startYear >= 1990 AND startYear < 2000 THEN '1990s'
        WHEN startYear >= 2000 AND startYear < 2010 THEN '2000s'
        WHEN startYear >= 2010 AND startYear < 2020 THEN '2010s'
        WHEN startYear >= 2020 AND startYear <= 2025 THEN '2020s'
        END AS decade,
        COUNT(DISTINCT tconst) AS all_count
    FROM read_csv_auto('{BASICS}', delim='\\t', header=True, nullstr='\\N')
    WHERE
        titleType = 'movie'
        AND startYear IS NOT NULL
    GROUP BY 1
),
titles_horror AS (
    SELECT CASE
        WHEN startYear >= 1910 AND startYear < 1920 THEN '1910s'
        WHEN startYear >= 1920 AND startYear < 1930 THEN '1920s'
        WHEN startYear >= 1930 AND startYear < 1940 THEN '1930s'
        WHEN startYear >= 1940 AND startYear < 1950 THEN '1940s'
        WHEN startYear >= 1950 AND startYear < 1960 THEN '1950s'
        WHEN startYear >= 1960 AND startYear < 1970 THEN '1960s'
        WHEN startYear >= 1970 AND startYear < 1980 THEN '1970s'
        WHEN startYear >= 1980 AND startYear < 1990 THEN '1980s'
        WHEN startYear >= 1990 AND startYear < 2000 THEN '1990s'
        WHEN startYear >= 2000 AND startYear < 2010 THEN '2000s'
        WHEN startYear >= 2010 AND startYear < 2020 THEN '2010s'
        WHEN startYear >= 2020 AND startYear <= 2025 THEN '2020s'
        END AS decade,
        COUNT(DISTINCT tconst) AS horror_count
    FROM read_csv_auto('{BASICS}', delim='\\t', header=True, nullstr='\\N')
    WHERE
        titleType = 'movie'
        AND genres LIKE '%Horror%'
        AND startYear IS NOT NULL
    GROUP BY 1
)
SELECT a.decade, a.all_count, h.horror_count, h.horror_count / a.all_count AS horror_share
FROM titles_all a 
INNER JOIN titles_horror h 
    ON a.decade = h.decade
ORDER BY a.decade DESC
"""

df_1 = con.execute(query1).df()
df_1.to_csv("clean_data/Q1.csv", index=False)

query2 = f"""
SELECT DISTINCT tconst, primaryTitle, startYear
FROM read_csv_auto('{BASICS}', delim='\\t', header=True, nullstr='\\N')
WHERE
    titleType = 'movie'
    AND genres LIKE '%Horror%'
    AND startYear IS NOT NULL
    AND startYear >= 2000
    AND startYear <= 2025

"""

df_2 = con.execute(query2).df()
df_2.to_csv("clean_data/Q2.csv", index=False)

'''
query = f"""
WITH horror_titles AS (
    SELECT
        tconst,
        titleType,
        primaryTitle,
        originalTitle,
        isAdult,
        startYear,
        endYear,
        runtimeMinutes,
        genres
    FROM read_csv_auto('{BASICS}', delim='\\t', header=True, nullstr='\\N')
    WHERE
        titleType = 'movie'
        AND genres LIKE '%Horror%'
        AND startYear IS NOT NULL
),
crew AS (
    SELECT
        tconst,
        directors
    FROM read_csv_auto('{CREW}', delim='\\t', header=True, nullstr='\\N')
),
ratings AS (
    SELECT
        tconst,
        averageRating,
        numVotes
    FROM read_csv_auto('{RATINGS}', delim='\\t', header=True, nullstr='\\N')
),
akas AS (
    SELECT
        titleId,
        ordering,
        title,
        region,
        language,
        types,
        attributes,
        isOriginalTitle
    FROM read_csv_auto('{AKAS}', delim='\\t', header=True, nullstr='\\N')
),
names AS (
    SELECT
        nconst,
        primaryName
    FROM read_csv_auto('{NAMES}', delim='\\t', header=True, nullstr='\\N')
),
expanded_directors AS (
    SELECT
        h.*,
        d.nconst AS director_nconst
    FROM horror_titles h
    LEFT JOIN crew c USING (tconst)
    LEFT JOIN UNNEST(string_split(c.directors, ',')) AS d(nconst) ON TRUE
)
SELECT
    e.tconst,
    e.primaryTitle,
    e.startYear,
    e.runtimeMinutes,
    e.genres,
    n.primaryName AS director_name,
    a.region,
    a.isOriginalTitle,
    r.averageRating,
    r.numVotes
FROM expanded_directors e
LEFT JOIN names n
    ON e.director_nconst = n.nconst
LEFT JOIN ratings r
    ON e.tconst = r.tconst
LEFT JOIN akas a
    ON e.tconst = a.tconst
WHERE e.director_nconst IS NOT NULL
ORDER BY e.startYear DESC
"""

df = con.execute(query).df()
df.to_csv("clean_data/imdb_horror_movies.csv", index=False)
'''

#print("Wrote:")
#print(" - imdb_horror_movies.csv")
print("df_2 rows:", len(df_2))
#print("Rows:", len(df))
