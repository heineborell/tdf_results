import pandas as pd
from sqlalchemy import create_engine, inspect, text

from scrape import activity_scrape, ride_scrape

if __name__ == "__main__":

    engine = create_engine(
        "mysql+mysqldb://root:Abrakadabra69!@127.0.0.1:3306/grand_tours"
    )
    conn = engine.connect()

    query = "SELECT DISTINCT(x.week), x.year FROM( SELECT `year`, EXTRACT(week FROM `date`) week FROM tdf_database) AS x "
    df = pd.read_sql_query(query, conn)
    df = df.loc[df["year"] == 2024]

    query_id = """
    SELECT * 
    FROM df_names AS y 
    LEFT JOIN (
        SELECT *
        FROM tdf_database
        WHERE stage LIKE %s AND `year` = %s
    ) AS x 
    ON y.`name` = x.`name`
    WHERE `year` IS NOT NULL
    """

    # Define parameters for the query
    params = ("Stage 1 %", 2024)

    # Execute the query
    df_id = pd.read_sql_query(query_id, engine, params=params)
    df_id.to_csv("2024_list.csv")
    # print(df_id["strava_id"].values[3])
    pro_id = df_id["strava_id"].values[97:]
    df_activity = pd.DataFrame(columns=["pro_id", "activity"])
    for id in pro_id:
        print(id)
        activity_list = []
        for year in df["year"].drop_duplicates().values:
            print(year)
            for week in df["week"].values:
                print(week)
                activity_list.extend(
                    ride_scrape.ride_scraper(pro_id=id, date=str(year) + str(week))
                )
                print(activity_list)
        activity_dict = {
            "pro_id": len(activity_list) * [id],
            "activity": activity_list,
        }
        df_activity = pd.concat([df_activity, pd.DataFrame.from_dict(activity_dict)])
        df_activity.to_csv("activity_list.csv")

    conn.close()
