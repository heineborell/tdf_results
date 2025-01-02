import subprocess

# import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, inspect, text

engine = create_engine("mysql+mysqldb://root:Abrakadabra69!@127.0.0.1:3306/grand_tours")
conn = engine.connect()

## Write the SQL statement inside a string
## then place in conn.execute

# results = conn.execute(text("select * from tdf_database"))

# print(inspect(engine).get_table_names())

## To print all the results of the query you can use
## fetchall()
# print(pd.DataFrame(results.fetchall(), columns=results.keys()))


# number one rider at every stage
query_1 = "SELECT*FROM(SELECT`year`, stage, `name`, `time`, ROW_NUMBER()OVER(PARTITION BY `year`, stage ORDER BY `time`) AS standing FROM tdf_database HAVING `time`IS NOT NULL ) AS x WHERE x.standing = 1 "
# avg speed of winner by stage
query_2 = "SELECT AVG(winner_avg_speed) as avg_speed, `year`, stage FROM tdf_database GROUP BY `year`, stage ORDER BY `year` "
# avg speed of winner by year
query_3 = "select x.`year`, avg(x.avg_speed) as speed from( SELECT AVG(winner_avg_speed) AS avg_speed, `year`, stage FROM tdf_database GROUP BY `year`, stage ORDER BY `year`) as x group by x.year "
# avg height climbed by year
query_4 = "SELECT AVG(x.vertical_meters) AS avg_climb, x.`year`FROM( SELECT * FROM tdf_database WHERE vertical_meters IS NOT NULL) AS x GROUP BY x.`year` "

query_5 = "SELECT x.`year`, x.stage, AVG(x.distance)OVER(PARTITION BY x.`date`) AS avgdist FROM( SELECT * FROM tdf_database WHERE distance IS NOT NULL) AS x "

# query_6 = "select * from strava_ids"

query_7 = """SELECT COUNT(f.strava_id), f.`year` FROM ( SELECT y.strava_id, y.`name`, x.`year` FROM df_names AS y LEFT JOIN ( SELECT * FROM tdf_database WHERE stage LIKE %s and `year` > %s ) AS x ON y.`name` = x.`name`) AS f GROUP BY f.`year` ORDER BY f.`year` """

query_8 = "select trim(cast(x.tdf_date as char)) as tdfdate from( SELECT DISTINCT(w.tdf_date) FROM ( SELECT Date_format( DATE, %s )AS tdf_date FROM tdf_database WHERE year= %s ) As w) as x"

query_9 = "SELECT p.activity_id, p.athlete_id, cast(p.`date` as char) as date, p.segment, l.stat from segments_data as p left join stats_data as l on l.activity_id=p.activity_id where p.`date` IN( select cast(x.tdf_date as CHAR) as tdfdate FROM( SELECT DISTINCT(w.tdf_date) FROM ( SELECT Date_format( DATE, %s) AS tdf_date FROM tdf_database WHERE year=%s) As w) as x) "

query_10 = """SELECT activity_id, athlete_id, f.`date`, f.elv_strava, test.vertical_meters, f.dist_strava, test.lower_bound, f.watt, stat, segment FROM ( SELECT x.activity_id, x.athlete_id, x.stat, x.segment, `date`, CAST( REGEXP_SUBSTR( x.watts, '[0-9]+') AS UNSIGNED) AS watt, CAST( REGEXP_SUBSTR( x.dist_strava, '[0-9]+')AS UNSIGNED) AS dist_strava, CAST( REGEXP_REPLACE( REGEXP_SUBSTR( x.elv_strava, '[0-9,]+'), ',', '') AS UNSIGNED) AS elv_strava FROM ( SELECT activity_id, athlete_id, stat, segment, `date`, JSON_EXTRACT( `stat`, "$.wap") AS watts, JSON_EXTRACT( `stat`, "$.elevation") AS elv_strava, JSON_EXTRACT( `stat`, "$.dist") AS dist_strava FROM ( SELECT p2.activity_id, p2.athlete_id, CAST( p2.`date` AS CHAR) AS DATE, p2.segment, l2.stat FROM segments_data AS p2 LEFT JOIN stats_data AS l2 ON l2.activity_id = p2.activity_id WHERE p2.`date`IN( SELECT CAST( x2.tdf_date AS CHAR) AS tdfdate FROM ( SELECT DISTINCT( w2.tdf_date) FROM ( SELECT Date_format( DATE, %s ) AS tdf_date FROM giro_results)AS w2)AS x2) )AS stravarider) AS x) AS f LEFT JOIN ( SELECT DISTINCT( stage), distance, vertical_meters, Date_format( `date`, %s )AS tdf_date, ROUND( distance * 0.2 + distance, 3)AS upper_bound, ROUND( distance - distance * 0.2, 3)AS lower_bound FROM giro_results ) AS test ON test.tdf_date = f.`date` WHERE f.dist_strava > test.lower_bound order by DATE"""

# df = pd.read_sql_query(query_3, conn)
# df2 = pd.read_sql_query(query_4, conn)
# df3 = pd.read_sql_query(query_5, conn)
## df4 = pd.read_sql_query(query_6, conn)
# df7 = pd.read_sql_query(query_7, conn, params=("Stage 1 %", 2001))
# df9 = pd.read_sql_query(query_9, conn, params=("%b %d %Y", 2024))
#
df10 = pd.read_sql_query(query_10, conn, params=("%b %e %Y", "%b %e %Y"))
# df["customer_name"] = df["customer_first_name"] + " " + df["customer_last_name"]
# df4["name"] = df4["name"].str.split(r"\s{2,}")[0] + df4["name"].str.split(r"\s{2,}")[1]
subprocess.run(["vd", "-f", "csv", "-"], input=df10.to_csv(index=False), text=True)

# plt.figure()
# plt.scatter(df2.year, df2.avg_climb)
## plt.scatter(df.year, df.speed)
# plt.show()


conn.close()
engine.dispose()
