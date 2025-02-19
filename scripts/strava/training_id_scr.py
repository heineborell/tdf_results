import getpass
import sqlite3

import pandas as pd

from grand_tours import ride_scrape

if __name__ == "__main__":
    username = getpass.getuser()

    grand_tour = "tdf"
    year = 2024

    conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")

    query_date = (
        f"SELECT DISTINCT x.week, x.year "
        f"FROM ( "
        f"    SELECT `year`, strftime('%W', `date`) AS week "
        f"    FROM {grand_tour}_results "
        f") AS x"
    )

    query_id = f" SELECT DISTINCT(athlete_id) FROM strava_table where tour_year = '{grand_tour}-{year}'"

    df = pd.read_sql_query(query_date, conn)
    start_week = df.loc[df["year"] == year]["week"].min()

    df = pd.read_sql_query(query_id, conn)

    pro_id = df["athlete_id"].values
    df_training = pd.DataFrame(columns=["athlete_id", "activity_id", "week", "tour_year"])
    for id in pro_id:
        print(id)
        for week in range(int(start_week), int(start_week) - 13, -1):
            activity_list = []
            print(week)
            activity_list.extend(ride_scrape.ride_scraper_local(pro_id=id, date=str(year) + str(week)))
            print(activity_list)
            activity_dict = {
                "athlete_id": len(activity_list) * [id],
                "activity_id": activity_list,
                "week": len(activity_list) * [week],
                "tour_year": len(activity_list) * [f"{grand_tour}-{year}"],
            }
            df_training = pd.concat([df_training, pd.DataFrame.from_dict(activity_dict)])
            df_training.to_csv(
                f"~/iCloud/Research/Data_Science/Projects/data/strava/training_list/training_list_{grand_tour}_{year}.csv"
            )
