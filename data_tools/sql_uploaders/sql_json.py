import getpass
import json
from pathlib import Path

from sqlalchemy import CHAR, JSON, Column, Float, Integer, String, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define your MySQL connection parameters
MYSQL_USER = "root"
MYSQL_PASSWORD = "Abrakadabra69!"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "grand_tours"


# Define database connection URL
DATABASE_URL = "mysql+pymysql://root:Abrakadabra69!@127.0.0.1:3306/grand_tours"

grand_tours = ["tdf", "giro"]
years = [2023]
username = getpass.getuser()

segment_range = Path(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segments/"
)
stat_range = Path(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/stats/"
)

# Initialize SQLAlchemy base
Base = declarative_base()


# Define the table model with activity_id as the primary key
class RawJSONData(Base):
    __tablename__ = "segments_data"
    activity_id = Column(
        "activity_id", String(20), primary_key=True, unique=True, nullable=False
    )
    athlete_id = Column("athlete_id", String(20))
    date = Column("date", String(20))
    distance = Column("distance", Float)
    segment = Column(JSON)

    def __init__(self, activity_id, athlete_id, date, distance, segment):
        self.activity_id = activity_id
        self.athlete_id = athlete_id
        self.date = date
        self.distance = distance
        self.segment = segment


# Define the table model with activity_id as the primary key
class RawJSONData_2(Base):
    __tablename__ = "stats_data"
    activity_id = Column(
        "activity_id", String(20), primary_key=True, unique=True, nullable=False
    )
    athlete_id = Column("athlete_id", String(20))
    stat = Column(JSON)

    def __init__(self, activity_id, athlete_id, stat):
        self.activity_id = activity_id
        self.athlete_id = athlete_id
        self.stat = stat


# Create database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE stats_data"))

    with engine.connect() as connection:
        connection.execute(text("DROP TABLE segments_data"))
except OperationalError:
    print("Tables do not exist")

# Create the table in the database (if not exists)
for grand_tour in grand_tours:
    for year in years:
        Base.metadata.create_all(engine)
        id_list = []
        for j in range(
            1, len(sorted(segment_range.glob(f"segment_{year}_{grand_tour}_*"))) + 1
        ):
            if j == 3 and year == 2024 and grand_tour == "tdf":
                with open(
                    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segments/segment_{year}_{grand_tour}_{j}.json",
                    "r",
                ) as f:
                    json_data = json.loads(f.read())

                for activity in json_data:
                    if activity["activity_id"] not in id_list:
                        row = RawJSONData(
                            str(activity["activity_id"]),
                            str(activity["athlete_id"]),
                            str(activity["date"])
                            .replace("June", "Jun")
                            .replace("July", "Jul"),
                            float(activity["distance"]),
                            activity["segments"][0],
                        )
                        session.add(row)
                        session.commit()
                        id_list.append(activity["activity_id"])
                        print(f"{j} segment {grand_tour} {year} uploaded")
                    else:
                        pass
            else:

                with open(
                    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segments/segment_{year}_{grand_tour}_{j}.json",
                    "r",
                ) as f:

                    json_data = json.loads(f.read())

                for activity in json_data["activities"]:
                    if activity["activity_id"] not in id_list:
                        row = RawJSONData(
                            str(activity["activity_id"]),
                            str(activity["athlete_id"]),
                            str(activity["date"])
                            .replace("June", "Jun")
                            .replace("July", "Jul"),
                            float(activity["distance"]),
                            activity["segments"][0],
                        )
                        session.add(row)
                        session.commit()
                        id_list.append(activity["activity_id"])
                        print(f"{j} segment {grand_tour} {year} uploaded")
                    else:
                        pass
        id_list = []
        for j in range(
            1, len(sorted(stat_range.glob(f"stat_{year}_{grand_tour}_*"))) + 1
        ):
            with open(
                f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/stats/stat_{year}_{grand_tour}_{j}.json",
                "r",
            ) as f:
                json_data = json.loads(f.read())

            for activity in json_data["stats"]:
                if activity["activity_id"] not in id_list:
                    row = RawJSONData_2(
                        str(activity["activity_id"]),
                        str(activity["athlete_id"]),
                        dict(list(activity.items())[2:]),
                    )
                    session.add(row)
                    session.commit()
                    id_list.append(activity["activity_id"])
                    print(f"{j} stats {grand_tour} {year} uploaded")
                else:
                    pass
print("JSON data uploaded successfully.")

query_giro = """(SELECT activity_id, athlete_id, f.`date`, f.elv_strava, test.vertical_meters, f.dist_strava, test.lower_bound, f.watt, stat, segment FROM ( SELECT x.activity_id, x.athlete_id, x.stat, x.segment, `date`, CAST( REGEXP_SUBSTR( x.watts, '[0-9]+') AS UNSIGNED) AS watt, CAST( REGEXP_SUBSTR( x.dist_strava, '[0-9]+')AS UNSIGNED) AS dist_strava, CAST( REGEXP_REPLACE( REGEXP_SUBSTR( x.elv_strava, '[0-9,]+'), ',', '') AS UNSIGNED) AS elv_strava FROM ( SELECT activity_id, athlete_id, stat, segment, `date`, JSON_EXTRACT( `stat`, "$.wap") AS watts, JSON_EXTRACT( `stat`, "$.elevation") AS elv_strava, JSON_EXTRACT( `stat`, "$.dist") AS dist_strava FROM ( SELECT p2.activity_id, p2.athlete_id, CAST( p2.`date` AS CHAR) AS DATE, p2.segment, l2.stat FROM segments_data AS p2 LEFT JOIN stats_data AS l2 ON l2.activity_id = p2.activity_id WHERE p2.`date`IN( SELECT CAST( x2.tdf_date AS CHAR) AS tdfdate FROM ( SELECT DISTINCT( w2.tdf_date) FROM ( SELECT Date_format( DATE, :s ) AS tdf_date FROM giro_results)AS w2)AS x2) )AS stravarider) AS x) AS f LEFT JOIN ( SELECT DISTINCT( stage), distance, vertical_meters, Date_format( `date`, :s )AS tdf_date, ROUND( distance * 0.2 + distance, 3)AS upper_bound, ROUND( distance - distance * 0.2, 3)AS lower_bound FROM giro_results ) AS test ON test.tdf_date = f.`date` WHERE f.dist_strava > test.lower_bound order by DATE) as giro_table """

query_tdf = """(SELECT activity_id, athlete_id, f.`date`, f.elv_strava, test.vertical_meters, f.dist_strava, test.lower_bound, f.watt, stat, segment FROM ( SELECT x.activity_id, x.athlete_id, x.stat, x.segment, `date`, CAST( REGEXP_SUBSTR( x.watts, '[0-9]+') AS UNSIGNED) AS watt, CAST( REGEXP_SUBSTR( x.dist_strava, '[0-9]+')AS UNSIGNED) AS dist_strava, CAST( REGEXP_REPLACE( REGEXP_SUBSTR( x.elv_strava, '[0-9,]+'), ',', '') AS UNSIGNED) AS elv_strava FROM ( SELECT activity_id, athlete_id, stat, segment, `date`, JSON_EXTRACT( `stat`, "$.wap") AS watts, JSON_EXTRACT( `stat`, "$.elevation") AS elv_strava, JSON_EXTRACT( `stat`, "$.dist") AS dist_strava FROM ( SELECT p2.activity_id, p2.athlete_id, CAST( p2.`date` AS CHAR) AS DATE, p2.segment, l2.stat FROM segments_data AS p2 LEFT JOIN stats_data AS l2 ON l2.activity_id = p2.activity_id WHERE p2.`date`IN( SELECT CAST( x2.tdf_date AS CHAR) AS tdfdate FROM ( SELECT DISTINCT( w2.tdf_date) FROM ( SELECT Date_format( DATE, :s ) AS tdf_date FROM tdf_results)AS w2)AS x2) )AS stravarider) AS x) AS f LEFT JOIN ( SELECT DISTINCT( stage), distance, vertical_meters, Date_format( `date`, :s )AS tdf_date, ROUND( distance * 0.2 + distance, 3)AS upper_bound, ROUND( distance - distance * 0.2, 3)AS lower_bound FROM tdf_results) AS test ON test.tdf_date = f.`date` WHERE f.dist_strava > test.lower_bound order by DATE) as tdf_table """

# Create database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE strava_table"))

except OperationalError:
    print("Tables do not exist")


query = (
    "CREATE TABLE strava_table AS SELECT * FROM "
    + query_tdf
    + " UNION SELECT * FROM "
    + query_giro
)

with engine.connect() as connection:
    stmt = text(query)
    stmt = stmt.bindparams(s="%b %e %Y")
    res = session.execute(stmt)
    print("strava_table formed.")
