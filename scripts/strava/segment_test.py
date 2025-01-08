import json

import matplotlib.pyplot as plt
import numpy as np

with open("segments_italy.json", "r") as f:
    json_data = json.loads(f.read())


ordered_list = sorted(json_data, key=lambda x: x["end_points"][1])
reduced_list = []

for i, elmt in enumerate(ordered_list):
    if i == 0:
        reduced_list.append(elmt["end_points"])
    elif i > 0:
        if float(reduced_list[-1][-1]) < float(elmt["end_points"][0]):
            reduced_list.append(elmt["end_points"])
        else:
            pass
print(reduced_list)


plt.figure()

for j, data in enumerate(reduced_list):
    if j % 2 == 0:
        plt.plot(data, [0.5, 0.5], linewidth=5)
    else:
        plt.plot(data, [0.51, 0.51], linewidth=5)

plt.ylim(0.49, 0.52)
plt.show()
