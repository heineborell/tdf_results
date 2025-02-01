import getpass
import gzip
import json
import pickle
import re


username = getpass.getuser()
with gzip.open(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/tdf_pickles/segment_6175322112_2018_tdf.pkl.gz",
    "rb",
) as fp:  # Pickling
    data = pickle.load(fp)


activity_id_list = [i[0][0][0] for i in data]
activity_type_list = [i[0][1][0] for i in data]

athelete_id_list = []
for key, value in enumerate(data):
    try:
        athelete_id_list.append(value[0][3][0])
    except IndexError:
        athelete_id_list.append("no id")
        print("No athelete id", key)

date_list = []
for key, value in enumerate(data):
    try:
        pattern = r"\b([A-Z][a-z]+) (\d{1,2}) (\d{4})\b"
        matching = re.findall(
            pattern,
            (value[0][2][0].split(",")[1]).strip()
            + " "
            + (value[0][2][0].split(",")[2].split(" ")[1]).strip(),
        )
        date_list.append(f"{matching[0][0]} {matching[0][1]} {matching[0][2]}")
    except IndexError:
        date_list.append("No date")
        print("no date", key)

distance_list = []
for i in data:
    try:
        distance_list.append(
            i[0][2][0].split("\n")[i[0][2][0].split("\n").index("Distance") - 1]
        )
    except (ValueError, IndexError):
        distance_list.append("No distance")


stat_dict_list = []

for i, no in enumerate(stat_dict_list):
    no = no.update({"athlete_id": athelete_id_list[i]})

stat_list = [i[0][-1] for i in data]
for p, stats in enumerate(stat_list):
    stat_dict = {}
    stat_dict.update(
        {
            "activity_id": activity_id_list[p],
            "athlete_id": athelete_id_list[p],
        }
    )
    try:
        stats.remove("Show More")
    except ValueError:
        print("No more stat", p)

    for i, stat in enumerate(stats):
        if stat == "Distance":
            stat_dict.update(
                {
                    "dist": stats[i - 1],
                }
            )
        if stat == "Moving Time":
            stat_dict.update({"move_time": stats[i - 1]})
        if stat == "Elevation":
            stat_dict.update({"elevation": stats[i - 1]})
        if stat == "Weighted Avg Power":
            stat_dict.update({"wap": stats[i - 1]})
        if stat == "total work":
            stat_dict.update({"tw": stats[i - 1]})
        if stat == "Avg Max":
            stat_dict.update({"avg_max": stats[i + 1]})
        if "Elapsed Time" in stat:
            stat_dict.update({"elapsed": stats[i].split(" ")[-1]})
        if stat == "Temperature":
            stat_dict.update({"temp": stats[i + 1]})
        if stat == "Humidity":
            stat_dict.update({"humd": stats[i + 1]})
        if stat == "Feels like":
            stat_dict.update({"feels": stats[i + 1]})
        if stat == "Wind Speed":
            stat_dict.update({"wind_speed": stats[i + 1]})
        if stat == "Wind Direction":
            stat_dict.update({"wind_direction": stats[i + 1]})
        if i == len(stats) - 1:
            stat_dict.update({"device": stats[i]})

    stat_dict_list.append(stat_dict)

    json_string = json.dumps(stat_dict_list)
    with open(
        f"stat.json",
        "w",
    ) as f:
        f.write(json_string)
