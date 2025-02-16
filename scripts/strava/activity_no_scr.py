import getpass
import sqlite3

import pandas as pd

from grand_tours import ride_scrape

if __name__ == "__main__":
    username = getpass.getuser()
    grand_tour = "giro"
    # grand_tour = "vuelta"
    year = 2020

    conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")

    query = (
        f"SELECT DISTINCT x.week, x.year "
        f"FROM ( "
        f"    SELECT `year`, strftime('%W', `date`) AS week "
        f"    FROM {grand_tour}_results "
        f") AS x"
    )
    df = pd.read_sql_query(query, conn)
    df = df.loc[df["year"] == year]
    print(df)

    query_id = f"""
    SELECT *
    FROM strava_names AS y
    LEFT JOIN (
        SELECT *
        FROM {grand_tour}_results
        WHERE stage LIKE ? AND `year` = ?
    ) AS x
    ON y.`name` = x.`name`
    WHERE x.`year` IS NOT NULL;
    """

    # Define parameters for the query
    params = ("Stage 1 %", year)

    # Execute the query
    df_id = pd.read_sql_query(query_id, conn, params=params)
    if df_id.size == 0:
        # Define parameters for the query
        params = ("Stage 2 %", year)
        df_id = pd.read_sql_query(query_id, conn, params=params)

    df_id.to_csv(f"{year}_{grand_tour}_list.csv")
    print(df_id["strava_id"].values[3])
    pro_id = df_id["strava_id"].values
    df_activity = pd.DataFrame(columns=["pro_id", "activity"])
    for id in pro_id:
        print(id)
        activity_list = []
        for year in df["year"].drop_duplicates().values:
            print(year)
            for week in df["week"].values:
                print(week)
                activity_list.extend(ride_scrape.ride_scraper(pro_id=id, date=str(year) + str(week)))
                print(activity_list)
        activity_dict = {
            "pro_id": len(activity_list) * [id],
            "activity": activity_list,
        }
        df_activity = pd.concat([df_activity, pd.DataFrame.from_dict(activity_dict)])
        df_activity.to_csv(
            f"~/iCloud/Research/Data_Science/Projects/data/strava/activity_list/activity_list_{grand_tour}_{year}.csv"
        )

    conn.close()
