from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define your MySQL connection parameters
MYSQL_USER = "root"
MYSQL_PASSWORD = "Abrakadabra69!"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "grand_tours"

# Define the database URL
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/your_database"

# Initialize the SQLAlchemy base and engine
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


# Define the tables
class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_id = Column(Integer, nullable=False)
    athlete_id = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    distance = Column(Float, nullable=False)

    # Relationships
    segments = relationship("Segment", back_populates="activity")


class Segment(Base):
    __tablename__ = "segments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    segment_name = Column(String(255), nullable=False)
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


# Insert data into the database
def insert_data(data):
    # Create an activity object
    activity = Activity(
        activity_id=data["activity_id"],
        athlete_id=data["athlete_id"],
        date=data["date"],
        distance=float(data["distance"]),
    )
    session.add(activity)
    session.flush()  # To get the activity ID before inserting segments

    # Insert segments
    for segment in data["segments"]:
        segment_obj = Segment(
            activity_id=activity.id,
            segment_name=segment["segment_name"],
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


# Call the function to insert data
insert_data(json_data)

print("Data inserted successfully!")
