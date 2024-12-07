import json

with open("segment_1_2024.json", "r") as f:
    json_data = json.loads(f.read())

print(json_data[0]["activities"][3].keys())
print(json_data[0]["activities"][3]["activity_id"])
print(json_data[0]["activities"][3]["segments"])

for activity in json_data[0]["activities"]:
    print(
        type(activity["activity_id"]),
        type(activity["athlete_id"]),
        type(activity["date"]),
        type(activity["distance"]),
        activity["segments"][0],
    )
