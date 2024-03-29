import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function is used to read the JSON files
    in the filepath into a pandas dataframe (example: data/song_data)
    to obtain data to insert into
    song and artist tables in the Sparkify database.

    Arguments:
        cur: the cursor object.
        filepath: log data file path.

    Depends on: sql_queries.py. Database and tables exist on server at
         connection string location.

    Test cases:
        Song data is inserted into the songs table.
        Artist data is inserted into the artists table.

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    # this operation produces a list within a list
    song_data_t = df.loc[:, ['song_id', 'title', 'artist_id', 'year',
        'duration']].values.tolist()

    # flatten the list within a list to avoid using executemany
    # (executemany is slower)
    song_data = []
    for sublist in song_data_t:
        for item in sublist:
            song_data.append(item)

    cur.execute(songs_table_insert, song_data)

    # insert artist record
    artist_data_t = df.loc[:, ['artist_id', 'artist_name',
        'artist_location', 'artist_latitude',
        'artist_longitude']].values.tolist()

    # Flatten the list within a list to avoid using executemany
    # (executemany is slower)
    artist_data = []
    for sublist in artist_data_t:
        for item in sublist:
            artist_data.append(item)

    cur.execute(artists_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This function is used to read the JSON files
    in the filepath (example: data/log_data) to obtain data to insert into
    the songplay, time and user tables in the Sparkify database.

    Arguments:
        cur: the cursor object.
        filepath: log data file path.

    Depends on: sql_queries.py. Database and tables exist on server at
         connection string location.

    Test cases:
        Data about songs played (from log files) is inserted
            into the songplay table.
        Time data is derived from the log file timestamp and is inserted
            into the time table.
        User data is derived from the log file and is inserted into the
            users table.

    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']
    df.sort_values(by='userId', inplace=True)
    df.drop_duplicates(subset='userId', keep=False, inplace=True)

    # convert timestamp column to datetime
    t = pd.to_datetime(df.loc[:, 'ts'], unit='ms')
    df['ts'] = t

    # insert time data records
    time_data = [
        t.dt.time, t.dt.hour, t.dt.day, t.dt.weekofyear,
        t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = [
        'start_time', 'hour', 'day', 'week', 'month',
        'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:, [
        'userId', 'firstName', 'lastName',
        'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(users_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song,
                                            row.artist, row.length))
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = [
            row.ts, row.userId, row.level, songid,
            artistid, row.sessionId, row.location,
            row.userAgent, row.song, row.artist]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: This function walks the filepath to find JSON files and
    calls two functions one at a time to process song and log file data.

    Arguments:
        cur: the cursor object.
        conn: the database connection string.
        filepath: log data file path.
        func: the name of a defined function to run (one of the two
        functions defined above, process_log_file or process_song_fil

    Dependency: sql_queries.py. Database and tables exist on server at
         connection string location.

    Test cases:
        The function reads as many files as it finds (i.e. filecount)
        for each of the two process functions.

    Returns:
        Prints file counts to terminal (no variables returned).
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Connect to the database and run the process data function for each set of files."""
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(
        cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(
        cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()