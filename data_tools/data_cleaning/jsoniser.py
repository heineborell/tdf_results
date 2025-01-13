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
json_data_list = []
for activity in json_data["activities"]:
    key_list = list(activity["segments"][0].keys())
    len_vecs = len(activity["segments"][0]["segment_no"])
    activity_list = []
    dict_list = []
    seg_no_list = []
    activity_dict = []
    for j in range(len_vecs):
        seg_no_list.append(activity["segments"][0]["segment_no"][j])
        if j % 9 == 0:
            pass
        else:
            for key in key_list[1:]:
                activity_list.append(activity["segments"][0][key][j])

                dict_list.append(dict(zip(key_list[1:] * len_vecs, activity_list)))

        activity_dict.append(dict(zip(seg_no_list * len_vecs, dict_list)))

    json_data = {
        "activity_id": activity["activity_id"],
        "athelete_id": activity["athlete_id"],
        "date": activity["date"],
        "distance": activity["distance"],
    }
    json_data.update(dict(zip(["segment_no"] * len(activity_dict), activity_dict)))
    json_data_list.append(json_data)

json_string = json.dumps(json_data_list)
with open(
    f"jsoniser_test.json",
    "w",
) as f:
    f.write(json_string)
