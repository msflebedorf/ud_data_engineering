
"""Description: This file contains SQL drop and create table statements 
statements as well as SQL insert statements for tables
in the database Sparkify.
It is called from the scripts create_tables.py and etl.py.
"""

# DROP TABLES

songplay_table_drop = """DROP TABLE IF EXISTS songplay;"""
users_table_drop = """DROP TABLE IF EXISTS users;"""
songs_table_drop = """DROP TABLE IF EXISTS songs;"""
artists_table_drop = """DROP TABLE IF EXISTS artists;"""
time_table_drop = """DROP TABLE IF EXISTS time;"""

# CREATE TABLES

songplay_table_create = """CREATE TABLE IF NOT EXISTS songplay
                         (songplay_id serial PRIMARY KEY,
                         start_dttime timestamp without time zone,
                         user_id int NOT NULL,
                         level varchar DEFAULT 'Free', 
                         song_id varchar,
                         artist_id varchar, 
                         session_id int NOT NULL,
                         location varchar DEFAULT 'Unknown',
                         user_agent varchar NOT NULL,
                         raw_song varchar, 
                         raw_artist varchar)
                         ; """

users_table_create = """CREATE TABLE IF NOT EXISTS users
                        (user_id int PRIMARY KEY,
                        first_name varchar, 
                        last_name varchar DEFAULT 'unknown',
                        gender char(1) DEFAULT 'U',
                        level varchar DEFAULT 'Free')
                        ; """

songs_table_create = """CREATE TABLE IF NOT EXISTS songs
                        (song_id varchar PRIMARY KEY,
                        title varchar NOT NULL,
                        artist_id varchar NOT NULL,
                        year int, duration numeric)
                        ; """

artists_table_create = """CREATE TABLE IF NOT EXISTS artists
                          (artist_id varchar PRIMARY KEY,
                          artist_name varchar NOT NULL,
                          location varchar DEFAULT 'Unknown',
                          latitude numeric, longitude numeric)
                          ; """

time_table_create = ("""CREATE TABLE IF NOT EXISTS time
                          (songplay_id serial PRIMARY KEY,
                          start_time time without time zone,
                          hour int, day int, week int, month int,
                          year int, weekday int)
                          ; """)

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplay (start_dttime, user_id,
                              level, song_id, artist_id,
                              session_id, location, user_agent,
                              raw_song, raw_artist)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                               %s, %s)
                            ; """)

users_table_insert = ("""INSERT INTO users(user_id, first_name,
                            last_name, gender,
                            level ON CONFLICT (user_id) 
                              DO UPDATE SET level=EXCLUDED.level)
                          VALUES (%s, %s, %s, %s, %s)
                          ; """)

songs_table_insert = ("""INSERT INTO songs (song_id, title, artist_id,
                           year, duration)
                          VALUES (%s, %s, %s, %s, %s)
                          ; """)

artists_table_insert = ("""INSERT INTO artists (artist_id, artist_name,
                             location, latitude, longitude)
                          VALUES (%s, %s, %s, %s, %s)
                          ; """)


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week,
                             month, year, weekday)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ; """)

# FIND SONGS

song_select = ("""SELECT s.song_id, a.artist_id
                FROM songs s, artists a
                WHERE a.artist_id = s.artist_id
                AND s.title = %s
                AND a.artist_name = %s
                AND s.duration = %s
                ; """)


# QUERY LISTS

create_table_queries = [
    songplay_table_create, users_table_create, songs_table_create,
    artists_table_create, time_table_create
]
drop_table_queries = [
    songplay_table_drop, users_table_drop, songs_table_drop,
    artists_table_drop, time_table_drop
]
