import json

from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define your MySQL connection parameters
MYSQL_USER = "root"
MYSQL_PASSWORD = "Abrakadabra69!"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "grand_tours"


engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# Initialize the SQLAlchemy base and engine
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Define the tables
class Activity(Base):
    __tablename__ = "activities"
    activity_id = Column(Integer, primary_key=True, nullable=False)
    athlete_id = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    distance = Column(Float, nullable=False)

    # Relationships
    segments = relationship("Segment", back_populates="activity")


class Segment(Base):
    __tablename__ = "segments"
    segment_name = Column(String(255), primary_key=True)  # Primary key
    activity_id = Column(Integer, ForeignKey("activities.activity_id"), nullable=False)
    segment_time = Column(String(50))
    segment_speed = Column(Float)
    watt = Column(String(50))
    heart_rate = Column(String(50))
    segment_distance = Column(Float)
    segment_vert = Column(String(50))
    segment_grade = Column(String(50))

    # Relationships
    activity = relationship("Activity", back_populates="segments")


# Create the tables
Base.metadata.create_all(engine)


# Function to load JSON data from a file
def load_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


# Function to insert data into the database
def insert_data(data):
    # Create an activity object
    activity = Activity(
        activity_id=data["activity_id"],
        athlete_id=data["athlete_id"],
        date=data["date"],
        distance=float(data["distance"]),
    )
    session.add(activity)

    # Insert segments
    for segment in data["segments"]:
        segment_obj = Segment(
            segment_name=segment["segment_name"],  # Primary key
            activity_id=activity.activity_id,  # Foreign key
            segment_time=segment.get("segment_time"),
            segment_speed=float(segment.get("segment_speed", 0)),
            watt=segment.get("watt"),
            heart_rate=segment.get("heart_rate"),
            segment_distance=float(segment.get("segment_distance", 0)),
            segment_vert=segment.get("segment_vert"),
            segment_grade=segment.get("segment_grade"),
        )
        session.add(segment_obj)

    session.commit()


# Load JSON data from the file
file_path = "segment.json"
json_data = load_json_file(file_path)

# Insert data into the database
insert_data(json_data)

print("Data from segment.json inserted successfully!")
