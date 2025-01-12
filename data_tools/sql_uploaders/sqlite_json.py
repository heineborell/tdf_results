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
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/segments/"
)
stat_range = Path(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/stats/"
)
details_range = Path(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/mapping/"
)
conn = sqlite3.connect(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/grand_tours.db"
)
cursor = conn.cursor()


try:
    with conn as connection:
        connection.execute("DROP TABLE stats_data")

    with conn as connection:
        connection.execute("DROP TABLE segments_data")

    with conn as connection:
        connection.execute("DROP TABLE segment_details_data")
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

cursor.execute(
    """
CREATE TABLE segment_details_data (
    segment_id INTEGER PRIMARY KEY,
    activity_id INTEGER,
    segment_name TEXT,
    category TEXT,
    hidden TEXT,
    end_points BLOB
)
"""
)

## Create the table in the database (if not exists)
id_list_stat = []
id_list_segment = []
id_list_details = []
for grand_tour in grand_tours:
    for year in years:
        for j in range(
            1, len(sorted(segment_range.glob(f"segment_{year}_{grand_tour}_*"))) + 1
        ):

            with open(
                f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/segments/segment_{year}_{grand_tour}_{j}.json",
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
                    # print(f"{j} segment {grand_tour} {year} uploaded")
                else:
                    pass

        for j in range(
            1, len(sorted(stat_range.glob(f"stat_{year}_{grand_tour}_*"))) + 1
        ):
            with open(
                f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/stats/stat_{year}_{grand_tour}_{j}.json",
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
                    # print(f"{j} stats {grand_tour} {year} uploaded")
                else:
                    pass

        for j in range(
            1,
            len(sorted(details_range.glob(f"segment_details_{year}_{grand_tour}_*")))
            + 1,
        ):
            with open(
                f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/mapping/segment_details_{year}_{grand_tour}_{j}.json",
                "r",
            ) as f:
                json_data = json.loads(f.read())

            for segment in json_data:
                if segment["segment_no"] not in id_list_details:
                    try:
                        segment["category"]
                    except KeyError:
                        segment["category"] = None

                    cursor.execute(
                        """ INSERT INTO segment_details_data  (segment_id, activity_id, segment_name, category, hidden, end_points) VALUES (?, ?, ?, ?, ?, ? ) """,
                        (
                            str(segment["segment_no"]),
                            str(segment["activity_no"]),
                            segment["segment_name"],
                            str(segment["category"]),
                            str(segment["hidden"]),
                            json.dumps(segment["end_points"]),
                        ),
                    )
                    id_list_details.append(segment["segment_no"])
                    print(f"{j} segment_details {grand_tour} {year} uploaded")
                else:
                    pass
print("JSON data uploaded successfully.")
conn.commit()
conn.close()
