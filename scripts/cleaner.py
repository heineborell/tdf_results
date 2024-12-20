import re

import pandas as pd

df = pd.read_csv(
    "~/iCloud/Research/Data_Science/Projects/data/pro_giro/pro_2024_1991.csv"
)


print(df.loc[df["time"].str.match(r"^\d{2}:\d{2}:\d{2}$")]["time"].str[:-3])

print(
    pd.to_datetime(
        df.loc[df["time"].str.match(r"^\d{2}:\d{2}:\d{2}$")]["time"].str[:-3],
        format="%M:%S",
    ).dt.seconds()
)
