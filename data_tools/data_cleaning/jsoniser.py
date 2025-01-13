import getpass
import json
import sqlite3
from pathlib import Path
from sqlite3 import OperationalError

from sqlalchemy import CHAR, JSON, Column, Float, Integer, String, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

grand_tour = "tdf"
year = 2024
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

with open(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/segments/segment_{year}_{grand_tour}_1.json",
    "r",
) as f:

    json_data = json.loads(f.read())

# print(json_data["activities"][2]["segments"][0]["segment_no"])
for activity in json_data["activities"][0:1]:
    key_list = list(activity["segments"][0].keys())
    len_vecs = len(activity["segments"][0]["segment_no"])
    activity_list = []
    for j in range(len_vecs):
        if j % 9 == 0:
            pass
        else:
            for key in key_list[1:]:
                activity_list.append(activity["segments"][0][key][j])

            print(dict(zip(key_list[1:] * len_vecs, activity_list)))
    # print(dict(zip(key_list[1:] * len_vecs, activity_list)))

# print(dict(zip(key_list * len_vecs, activity["segments"][0][key][j])))


## Create the table in the database (if not exists)
