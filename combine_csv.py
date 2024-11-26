import subprocess

import numpy as np
import pandas as pd

df1 = pd.read_csv("protdf_2024_1919.csv")
df2 = pd.read_csv("protdf_1919_1903.csv")


df = pd.concat([df1, df2]).drop(
    columns=[
        "Classification:",
        "Race category:",
        "Points scale:",
        "UCI scale:",
        "Parcours type:",
        "Race ranking:",
    ]
)

#  year column
df["year"] = pd.to_datetime(df["year"]).dt.year  # setting year as datetime

# time column
df = df.drop(
    df.loc[df["time"].str.contains(r"-\d+") == True].index
)  # 45 records have - time infront of them for some reason I don't understand, so I had to drop them out
df["time"] = df["time"].replace("-", np.nan)  # replace dnf by nan
df["time"] = pd.to_numeric(df["time"])

# date column
df = df.rename(columns={"Date:": "date"})
df["date"] = pd.to_datetime(df["date"])

# start time
df = df.rename(columns={"Start time:": "start_time"})

# avg speed winner
df = df.rename(columns={"Avg. speed winner:": "winner_avg_speed"})
df["winner_avg_speed"] = df["winner_avg_speed"].replace(
    "-", np.nan
)  # replace dnf by nan
df["winner_avg_speed"] = df["winner_avg_speed"].str.split(" ").str[0]
df["winner_avg_speed"] = pd.to_numeric(df["winner_avg_speed"])
# distance
df = df.rename(columns={"Distance:": "distance"})
df["distance"] = df["distance"].str.split(" ").str[0]
df["distance"] = pd.to_numeric(df["distance"])

# profile score
df = df.rename(columns={"ProfileScore:": "profile_score"})
df["profile_score"] = df["profile_score"].replace("Na", np.nan)  # replace dnf by nan
df["profile_score"] = pd.to_numeric(df["profile_score"])

# vertical meters
df = df.rename(columns={"Vertical meters:": "vertical_meters"})
df["vertical_meters"] = df["vertical_meters"].replace(
    "Na", np.nan
)  # replace dnf by nan
df["vertical_meters"] = pd.to_numeric(df["vertical_meters"])

# startlist quality
df = df.rename(columns={"Startlist quality score:": "startlist_quality"})
df["startlist_quality"] = df["startlist_quality"].replace(
    "Na", np.nan
)  # replace dnf by nan
df["startlist_quality"] = pd.to_numeric(df["startlist_quality"])

# won how
df = df.rename(columns={"Won how:": "won_how"})
df["won_how"] = df["won_how"].replace("Na", np.nan)  # replace dnf by nan

# avg temperature
df = df.rename(columns={"Avg. temperature:": "avg_temperature"})
df["avg_temperature"] = df["avg_temperature"].str.split(" ").str[0]
df["avg_temperature"] = df["avg_temperature"].replace(
    "Na", np.nan
)  # replace dnf by nan
df["avg_temperature"] = pd.to_numeric(df["avg_temperature"])

subprocess.run(
    ["vd", "-f", "csv", "-"], input=df.to_csv(index=False), text=True
)  # cool way to print out tables using visidata
