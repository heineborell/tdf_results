import json

with open("segment_2024_tdf_short_2.json", "r") as f:
    json_data = json.loads(f.read())

for activity in json_data["activities"]:
    for segment in activity["segments"]:
        del segment["segment_name"]


json_data = json.dumps(json_data)
with open(
    f"segment_2024_tdf_short_2_new.json",
    "w",
) as f:
    f.write(json_data)
