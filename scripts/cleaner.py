import re
from datetime import datetime, timedelta

import pandas as pd

df = pd.read_csv(
    "~/iCloud/Research/Data_Science/Projects/data/pro_giro/pro_2024_1991.csv"
)


index_list = df.loc[df["time"].str.match(r"^\d{2}:\d{2}:\d{2}$")].index
for i in index_list:
    t = datetime.strptime(df.iloc[i]["time"][:-3], "%M:%S")
    df.loc[i, "time"] = int(
        timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
    )
    df.loc[i, "time"] = df.loc[i, "time"] + 23852
    print(df.loc[i, "time"])

df.to_csv("~/iCloud/Research/Data_Science/Projects/data/pro_giro/pro_2024_1991_edt.csv")
