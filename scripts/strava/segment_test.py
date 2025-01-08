import json

import matplotlib.pyplot as plt
import numpy as np

with open("segments_italy.json", "r") as f:
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

graph_list = []
for i in reduced_list:
    graph_list.extend(i["end_points"])
print(len(reduced_list))
print(len(ordered_list))
print(graph_list)


plt.figure()

for i in reduced_list:
    plt.plot(i["end_points"], [1, 1], linewidth=5)
for i in ordered_list:
    plt.plot(i["end_points"], [0.5, 0.5], linewidth=5)

plt.show()
