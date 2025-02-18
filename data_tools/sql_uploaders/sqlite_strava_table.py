import getpass
import sqlite3

from rich import print

grand_tours = ["giro", "tdf"]
username = getpass.getuser()


conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")
cursor = conn.cursor()


try:
    with conn as connection:
        connection.execute("DROP TABLE strava_table")

except sqlite3.OperationalError:
    print("Tables do not exist")

query_dict = {}
for tour in grand_tours:
    query_dict.update(
        {
            f"{tour}": f"""
        SELECT
            t3.activity_id,
            t3.athlete_id,
            t3.tour_year,
            t3.strava_distance,
            t1.distance AS official_distance,
            t3.DATE,
            t1.stage,
            t3.segment,
            t3.stat
        FROM (
            SELECT
                t2.activity_id,
                t2.athlete_id,
                CAST(t2.`date` AS TEXT) AS DATE,
                t2.tour_year,
                t2.distance AS strava_distance,
                t2.segment,
                l.stat
            FROM segments_data AS t2
            LEFT JOIN stats_data AS l
                ON l.activity_id = t2.activity_id
        ) AS t3
        INNER JOIN (
            SELECT DISTINCT
                (
                    substr(
                        "--JanFebMarAprMayJunJulAugSepOctNovDec",
                        strftime("%m", DATE) * 3,
                        3
                    ) || ' ' || CAST(strftime('%d', DATE) AS INTEGER) || ' ' || strftime('%Y', DATE)
                ) AS {tour}_date,
                stage,
                distance
            FROM {tour}_results
        ) AS t1
        ON t1.{tour}_date = t3.DATE
        WHERE (t1.distance - t1.distance * 0.2) < t3.strava_distance
        AND t3.strava_distance < (t1.distance * 0.2 + t1.distance);
        """
        }
    )

print(query_dict["giro"])

# Remove semicolons from the query_dict strings and any trailing whitespace
for tour in grand_tours:
    query_dict[tour] = query_dict[tour].strip().rstrip(";")

# Then construct and execute the final query
query = f"CREATE TABLE strava_table AS {query_dict['tdf']} UNION ALL {query_dict['giro']}"
cursor.execute(query)
print("strava_table created.")


conn.commit()
conn.close()
