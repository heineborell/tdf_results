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

# grand_tour = "giro"
grand_tour = "tdf"
year = 2024
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
Base.metadata.create_all(engine)
id_list = []
for j in range(
    1, len(sorted(segment_range.glob(f"segment_{year}_{grand_tour}_*"))) + 1
):
    if j == 3 and year == 2024:
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
                    str(activity["date"]).replace("June", "Jun").replace("July", "Jul"),
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

        for activity in json_data[0]["activities"]:
            if activity["activity_id"] not in id_list:
                row = RawJSONData(
                    str(activity["activity_id"]),
                    str(activity["athlete_id"]),
                    str(activity["date"]).replace("June", "Jun").replace("July", "Jul"),
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
for j in range(1, len(sorted(stat_range.glob(f"stat_{year}_{grand_tour}_*"))) + 1):
    with open(
        f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/stats/stat_{year}_{grand_tour}_{j}.json",
        "r",
    ) as f:
        json_data = json.loads(f.read())

    for activity in json_data[0]["stats"]:
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
