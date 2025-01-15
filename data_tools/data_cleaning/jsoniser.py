import getpass
import json
from pathlib import Path

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
    f"/Users/dmini/Projects/TDF/scripts/strava/segment_2024_tdf_1.json",
    "r",
) as f:
    json_data = json.loads(f.read())
json_data_list = []
for activity in json_data["activities"]:
    key_list = list(activity["segments"][0].keys())
    len_vecs = len(activity["segments"][0]["segment_name"])
    activity_list = []
    dict_list = []
    seg_no_list = []
    activity_dict = []
    for j in range(len_vecs):
        seg_no_list.append(activity["segments"][0]["segment_name"][j])
        if j % 9 == 0:
            pass
        else:
            for key in key_list[1:]:
                activity_list.append(activity["segments"][0][key][j])

                dict_list.append(dict(zip(key_list[1:] * len_vecs, activity_list)))

        activity_dict.append(dict(zip(seg_no_list * len_vecs, dict_list)))

    json_data = {
        "activity_id": activity["activity_id"],
        "athlete_id": activity["athlete_id"],
        "date": activity["date"],
        "distance": activity["distance"],
    }
    json_data.update(dict(zip(["segments"] * len(activity_dict), activity_dict)))
    json_data_list.append(json_data)

json_string = json.dumps(json_data_list)
with open(
    f"jsoniser_test_2.json",
    "w",
) as f:
    f.write(json_string)
