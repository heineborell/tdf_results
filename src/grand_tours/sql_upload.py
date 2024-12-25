import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.types import *


class SqlUploader:
    def __init__(
        self, mysql_user, mysql_password, mysql_host, mysql_port, mysql_database
    ) -> None:
        """Initialize the class with server and login info"""
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_database = mysql_database

    def create_db(self):
        """Create Database"""
        connection = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.mysql_database}")
        print(f"{self.mysql_database} database created.")
        cursor.close()
        connection.close()

    def clean_pro_table(self, table_list):
        """Clean the tables from procycling stats"""
        self.df = pd.concat([pd.read_csv(k) for k in table_list]).drop(
            columns=[
                "Unnamed: 0",
                "Classification:",
                "Race category:",
                "Points scale:",
                "UCI scale:",
                "Parcours type:",
                "Race ranking:",
            ]
        )
        #  year column
        self.df["year"] = pd.to_numeric(self.df["year"])

        # stage column
        self.df["stage"] = self.df["stage"].str.split("|").str[0]

        # time column
        self.df = self.df.drop(
            self.df.loc[self.df["time"].str.contains(r"-\d+") == True].index
        )  # 45 records have - time infront of them for some reason I don't understand, so I had to drop them out
        self.df["time"] = self.df["time"].replace("-", np.nan)  # replace dnf by nan
        self.df["time"] = pd.to_numeric(self.df["time"])

        # date column
        self.df = self.df.rename(columns={"Date:": "date"})
        self.df["date"] = pd.to_datetime(self.df["date"])

        # start time
        self.df = self.df.rename(columns={"Start time:": "start_time"})

        # avg speed winner
        self.df = self.df.rename(columns={"Avg. speed winner:": "winner_avg_speed"})
        self.df["winner_avg_speed"] = self.df["winner_avg_speed"].replace(
            "-", np.nan
        )  # replace dnf by nan
        self.df["winner_avg_speed"] = self.df["winner_avg_speed"].str.split(" ").str[0]
        self.df["winner_avg_speed"] = pd.to_numeric(self.df["winner_avg_speed"])
        # distance
        self.df = self.df.rename(columns={"Distance:": "distance"})
        self.df["distance"] = self.df["distance"].str.split(" ").str[0]
        self.df["distance"] = pd.to_numeric(self.df["distance"])

        # profile score
        self.df = self.df.rename(columns={"ProfileScore:": "profile_score"})
        self.df["profile_score"] = self.df["profile_score"].replace(
            "Na", np.nan
        )  # replace dnf by nan
        self.df["profile_score"] = pd.to_numeric(self.df["profile_score"])

        # vertical meters
        self.df = self.df.rename(columns={"Vertical meters:": "vertical_meters"})
        self.df["vertical_meters"] = self.df["vertical_meters"].replace(
            "Na", np.nan
        )  # replace dnf by nan
        self.df["vertical_meters"] = pd.to_numeric(self.df["vertical_meters"])

        # startlist quality
        self.df = self.df.rename(
            columns={"Startlist quality score:": "startlist_quality"}
        )
        self.df["startlist_quality"] = self.df["startlist_quality"].replace(
            "Na", np.nan
        )  # replace dnf by nan
        self.df["startlist_quality"] = pd.to_numeric(self.df["startlist_quality"])

        # won how
        self.df = self.df.rename(columns={"Won how:": "won_how"})
        self.df["won_how"] = self.df["won_how"].replace(
            "Na", np.nan
        )  # replace dnf by nan

        # avg temperature
        self.df = self.df.rename(columns={"Avg. temperature:": "avg_temperature"})
        self.df["avg_temperature"] = self.df["avg_temperature"].str.split(" ").str[0]
        self.df["avg_temperature"] = self.df["avg_temperature"].replace(
            "Na", np.nan
        )  # replace dnf by nan
        self.df["avg_temperature"] = pd.to_numeric(self.df["avg_temperature"])

        return self.df

    def direct_loader(self, data):
        """Directly Load DataFrame without cleaning"""
        self.df = data
        return self.df

    def csv_uploader(self, df_schema, table_name):
        """Upload the dataframe defined (either cleaned or direct)"""
        engine = create_engine(
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

        with engine.connect() as connection:
            self.df.to_sql(
                table_name,
                connection,
                if_exists="replace",
                dtype=df_schema,
                index=False,
            )

        print("Database Uploaded")

        connection.close()
        engine.dispose()
