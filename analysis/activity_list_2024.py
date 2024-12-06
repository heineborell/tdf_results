import subprocess

import pandas as pd

df_1 = pd.read_csv("../scripts/activity_list_1.csv")
df_2 = pd.read_csv("../scripts/activity_list_2.csv")
df_3 = pd.read_csv("../scripts/activity_list_3.csv")
df_4 = pd.read_csv("../scripts/activity_list_4.csv")


df = pd.concat([df_1, df_2, df_3, df_4]).drop_duplicates(subset=["activity"])
subprocess.run(["vd", "-f", "csv", "-"], input=df.to_csv(index=False), text=True)
