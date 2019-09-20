### Introduction ###

This project was initiated to facilitate analysis by staff at the streaming music provider, Sparkify. Staff will be able to query a database to answer questions about the customer's listening habits and the popularity of artists and songs in their song library. The project includes creating and loading data into a PostgreSQL database using an ETL pipeline written in Python.


### Data sources ###

There are two major data sources which are loaded into the database. The data sources are JSON files.
1) Data about songs and artists.
2) Data from logs created when customers (users) play songs using the Sparkify service during the month of November 2018 only.

### Schema ###

The following five tables are part of the Sparkify database. I am using a basic data warehouse schema to facilitate the queries that I have identified that Sparkify staff might want to run. The basic schema consists of a fact table (songplay) and four related dimension tables.

1. Songs. Primary key: Song ID (character column). Includes year that the song was published and its duration (for example).
2. Artists. The Songs and Artists tables have artist ID (a character column) in common.
3. Users. Primary key: User ID. Originates from log files. References user_id in songplay table.
4. Songplay. The fact table. Data includes user_id, browser type (user agent) and playback start date and time. Joins to the users dimension table. Should join to the artists and songs tables, but an issue in the downloaded test data prevents that (see Issues, below). Data originates from log files.
5. Time. A dimension table that makes it easy to access the month, day, week, year of the playback start timestamp as contained in the songplay table. Data originates from log files.

Because this database is for analytical purposes, we want to load data even if non-critical values are missing. For this reason, rather than throw errors by using 'NOT NULL' constraint for non-critical values, we will use a DEFAULT value. Often 
'Unknown' will be used as a default rather than allowing a NULL default so that results are easier for the end use to read.

### Process ###

1. Open a terminal session and run the python script create_tables.py to create a database called Sparkify and create the tables listed above.
2. In the terminal session, run the python script etl.py to read input files and insert rows into the appropriate tables. The script etl.py uses SQL stored in sql_queries.py

### Dependencies ###

Connectivity to a PostgreSQL database server.
Python version: Tested with 3.6
Python, pandas library versions: Current versions compatible with Python 3.6, as of September 2019

### Issues ###

As of Sept 2019: When running locally with downloaded test data, the song titles, artist names and song duration in the song and artist data files do not match (join to) the song titles, artist's name or length in the log data files. Therefore the columns for artist_id and song_id in the songplay table contain None/NULL values.

Two columns from the raw log data have been loaded to the songplay table to facilitate further investigation. Those columns are raw_artist and raw_song.

### Future development ###

1. Identify the cause and fix the issue outlined above.

2. Add a 'Genre' dimension table so that songs can be grouped and analyzed based on genre. Information gained from analysis based on genre could be used to target promotions of the streaming service to specific audiences.


### Sample queries ###

/* What are the five busiest days for streaming songs in November 2018? */


SELECT COUNT(t.songplay_id) AS play_count, t.day
FROM time t
WHERE t.month = 11 AND t.year = 2018
GROUP by t.day
ORDER BY play_count desc
LIMIT 5
;


/* Which artists have the most songs in the songs library (show top 5) */
SELECT a.artist_name as artist, count(s.song_id) as song_count
FROM songs s INNER JOIN artists a
ON a.artist_id = s.artist_id
GROUP BY a.artist_name
ORDER BY song_count desc
LIMIT 5;


/* Which artists appear most frequently in the songs played data?  (Show top 5) */
SELECT sp.sp_artist as artist, COUNT(sp.songplay_id) as song_count
FROM songplay sp
GROUP BY artist
ORDER BY song_count desc
LIMIT 5;


The top result of this query is 'Coldplay'.
The query below shows that 'Coldplay' is not present in the song data used to load the artists table.
/* Does the top artist from songplay appear in the artists table? */
SELECT artist_id FROM artists WHERE artist_name like 'Cold%'