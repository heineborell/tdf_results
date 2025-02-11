
import getpass
import gzip
import pickle
import re

username = getpass.getuser()
with gzip.open(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/giro_pickles/segment_6206058496_2017_giro.pkl.gz",
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
        print(i[0][2][0].split("\n")[i[0][2][0].split("\n").index("Distance") - 1])
        distance_list.append(
            i[0][2][0].split("\n")[i[0][2][0].split("\n").index("Distance") - 1]
        )
    except (ValueError, IndexError):
        distance_list.append("No distance")



