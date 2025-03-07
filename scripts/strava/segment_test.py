"""Module for scraping some segment details like endpoints, category"""

import json
from pathlib import Path

path = Path(
    "/Users/deniz/iCloud/Research/Data_Science/Projects/data/strava/segment_details/segment_details_2022_tdf.json"
)
if path.exists():
    with open(path, "rb") as fp:  # Pickling
        dict_list = json.loads(fp.read())
else:
    dict_list = []

print(dict_list)

prev_list = []
for i in dict_list:
    prev_list.append([i["activity_no"], i["hidden"], i["segment_number"]])

print(prev_list)
