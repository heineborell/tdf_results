import getpass
import sqlite3

import pandas as pd

username = getpass.getuser()


conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")
cursor = conn.cursor()


try:
    with conn as connection:
        connection.execute("DROP TABLE strava_names")

except sqlite3.OperationalError:
    print("Tables do not exist")

cursor.execute(
    """
CREATE TABLE strava_names (
    athlete_id INTEGER PRIMARY KEY,
    name TEXT
)
"""
)

df_ids = pd.concat(
    [
        pd.read_csv(
            f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/strava_ids.csv",
            usecols=["name", "strava_id"],
            index_col=False,
        ).dropna(),
        pd.read_csv(
            f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/strava_ids_2.csv",
            usecols=["name", "strava_id"],
            index_col=False,
        ).dropna(),
    ],
    ignore_index=True,
)


## Create the table in the database (if not exists)
id_list = []
for index in list(df_ids.index):
    if df_ids["strava_id"][index] not in id_list:
        cursor.execute(
            """ INSERT INTO strava_names (athlete_id, name) VALUES (?, ?) """,
            (int(df_ids["strava_id"][index]), str(df_ids["name"][index])),
        )
        id_list.append(df_ids["strava_id"][index])
    else:
        pass

conn.commit()
conn.close()
