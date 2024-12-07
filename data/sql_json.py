import json

from sqlalchemy import CHAR, JSON, Column, Float, Integer, String, create_engine
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

# Initialize SQLAlchemy base
Base = declarative_base()


# Define the table model with activity_id as the primary key
class RawJSONData(Base):
    __tablename__ = "raw_json_data"
    activity_id = Column(
        "activity_id", String(20), primary_key=True, unique=True, nullable=False
    )
    athlete_id = Column("athlete_id", String(20))
    date = Column("date", String(20))
    distance = Column("distance", Float)
    data = Column(JSON, nullable=False)

    # data = Column(JSON, nullable=False)
    def __init__(self, activity_id, athlete_id, date, distance, data):
        self.activity_id = activity_id
        self.athlete_id = athlete_id
        self.date = date
        self.distance = distance
        self.data = data


# Create database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create the table in the database (if not exists)
Base.metadata.create_all(engine)


# Load and insert JSON data into the database
with open("segment_1_2024.json", "r") as f:
    json_data = json.loads(f.read())

for activity in json_data[0]["activities"]:
    row = RawJSONData(
        str(activity["activity_id"]),
        str(activity["athlete_id"]),
        str(activity["date"]),
        float(activity["distance"]),
        activity["segments"][0],
    )
    session.add(row)
    session.commit()


print("JSON data uploaded successfully.")
