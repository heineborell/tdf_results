import getpass
import json
import sqlite3
from pathlib import Path
from sqlite3 import OperationalError

from sqlalchemy import CHAR, JSON, Column, Float, Integer, String, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

grand_tours = ["tdf"]
years = [2024]
username = getpass.getuser()

segment_range = Path(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segments/"
)
stat_range = Path(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/stats/"
)


# /Users/dmini/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/segments

conn = sqlite3.connect(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/grand_tours.db"
)
cursor = conn.cursor()


try:
    with conn as connection:
        connection.execute("DROP TABLE stats_data")

    with conn as connection:
        connection.execute("DROP TABLE segments_data")
except sqlite3.OperationalError:
    print("Tables do not exist")

cursor.execute(
    """
CREATE TABLE segments_data (
    activity_id INTEGER PRIMARY KEY,
    athlete_id INTEGER,
    date TEXT,
    distance FLOAT,
    segment BLOB
)
"""
)

cursor.execute(
    """
CREATE TABLE stats_data (
    activity_id INTEGER PRIMARY KEY,
    athlete_id INTEGER,
    stat BLOB
)
"""
)


## Create the table in the database (if not exists)
id_list_stat = []
id_list_segment = []
for grand_tour in grand_tours:
    for year in years:
        print(len(sorted(segment_range.glob(f"segment_{year}_{grand_tour}_*"))) + 1)
        for j in range(
            1, len(sorted(segment_range.glob(f"segment_{year}_{grand_tour}_*"))) + 1
        ):

            with open(
                f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segments/segment_{year}_{grand_tour}_{j}.json",
                "r",
            ) as f:

                json_data = json.loads(f.read())

            for activity in json_data["activities"]:
                if activity["activity_id"] not in id_list_segment:
                    cursor.execute(
                        """ INSERT INTO segments_data (activity_id, athlete_id, date, distance, segment) VALUES (?, ?, ?, ?, ?) """,
                        (
                            str(activity["activity_id"]),
                            str(activity["athlete_id"]),
                            str(activity["date"])
                            .replace("June", "Jun")
                            .replace("July", "Jul")
                            .replace("August", "Aug")
                            .replace("September", "Sep"),
                            float(activity["distance"]),
                            json.dumps(activity["segments"][0]),
                        ),
                    )
                    id_list_segment.append(activity["activity_id"])
                    print(f"{j} segment {grand_tour} {year} uploaded")
                else:
                    pass

        for j in range(
            1, len(sorted(stat_range.glob(f"stat_{year}_{grand_tour}_*"))) + 1
        ):
            with open(
                f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/stats/stat_{year}_{grand_tour}_{j}.json",
                "r",
            ) as f:
                json_data = json.loads(f.read())

            for activity in json_data["stats"]:
                if activity["activity_id"] not in id_list_stat:
                    cursor.execute(
                        """ INSERT INTO stats_data (activity_id, athlete_id, stat) VALUES (?, ?, ? ) """,
                        (
                            str(activity["activity_id"]),
                            str(activity["athlete_id"]),
                            json.dumps(dict(list(activity.items())[2:])),
                        ),
                    )
                    id_list_stat.append(activity["activity_id"])
                    print(f"{j} stats {grand_tour} {year} uploaded")
                else:
                    pass
print("JSON data uploaded successfully.")
conn.commit()
conn.close()
