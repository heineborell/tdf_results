import subprocess

import matplotlib.pyplot as plt
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

query_6 = "select * from strava_ids"

df = pd.read_sql_query(query_3, conn)
df2 = pd.read_sql_query(query_4, conn)
df3 = pd.read_sql_query(query_5, conn)
df4 = pd.read_sql_query(query_6, conn)
# df["customer_name"] = df["customer_first_name"] + " " + df["customer_last_name"]
df4["name"] = df4["name"].str.split(r"\s{2,}")[0] + df4["name"].str.split(r"\s{2,}")[1]
subprocess.run(["vd", "-f", "csv", "-"], input=df4.to_csv(index=False), text=True)

# plt.figure()
# plt.scatter(df2.year, df2.avg_climb)
## plt.scatter(df.year, df.speed)
# plt.show()


conn.close()
engine.dispose()
