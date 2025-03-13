import subprocess

import pandas as pd

df_1 = pd.read_csv("../scripts/activity_list_1.csv")
df_2 = pd.read_csv("../scripts/activity_list_2.csv")
df_3 = pd.read_csv("../scripts/activity_list_3.csv")
df_4 = pd.read_csv("../scripts/activity_list_4.csv")

js_1 = pd.read_json("../data/segment_1_2024.json")
js_2 = pd.read_json("../data/segment_2_2024.json")


for i in js_1["activities"]:
    print(i)


df = pd.concat([df_1, df_2, df_3, df_4]).drop_duplicates(subset=["activity"])
json = pd.concat([js_1, js_2])

# df.to_csv("../activity_list_2024.csv")
subprocess.run(["vd", "-f", "json", "-"], input=json.to_json(index=False), text=True)
