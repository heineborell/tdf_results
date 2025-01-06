import json

with open("selection.json", "r") as f:
    json_data = json.loads(f.read())


ordered_list = sorted(json_data, key=lambda x: x["end_points"][1])
reduced_list = []
for i, elmt in enumerate(ordered_list):
    if i == 0:
        reduced_list.append(elmt)
    elif i > 0:
        if reduced_list[-1]["end_points"][1] < float(elmt["end_points"][0]):
            reduced_list.append(elmt)
        else:
            pass

for i in reduced_list:
    print(i)
print(len(reduced_list))
print(len(ordered_list))
