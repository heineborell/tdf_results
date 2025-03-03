import getpass
import json
import sqlite3
from pathlib import Path

from rich import print

from grand_tours import logger_config

grand_tours = ["tdf"]
years = [2024, 2023]
username = getpass.getuser()


details_range = Path(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segment_details/")

conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/segment_details.db")
cursor = conn.cursor()
logger = logger_config.setup_logger(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/segment_details.log")


try:
    with conn as connection:
        connection.execute("DROP TABLE segment_details_data")

except sqlite3.OperationalError:
    print("Tables do not exist")


cursor.execute(
    """
CREATE TABLE segment_details_data (

   activity_id INTEGER,
   stage TEXT,
   tour_year TEXT,
   segment_id INTEGER,
   segment_name TEXT,
   end_points BLOB,
   total_length INTEGER,
   category TEXT,
   hidden TEXT
)
"""
)

#
# ## Create the table in the database (if not exists)
id_list_details = []
for grand_tour in grand_tours:
    for year in years:
        print(f"[bold yellow] ----------------{grand_tour}, {year}-------------- [/bold yellow]")

        with open(
            f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segment_details/segment_details_{year}_{grand_tour}.json",
            "r",
        ) as f:
            json_data = json.loads(f.read())

        for segment in json_data:
            if segment["segment_no"] not in id_list_details:
                cursor.execute(
                    """
                    INSERT INTO segment_details_data (
                        activity_id, stage, tour_year, segment_id, segment_name,
                        end_points, total_length, category, hidden
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(segment["activity_no"]),
                        str(segment["stage"]),
                        str(segment["tour_year"]),
                        int(segment["segment_no"]),
                        segment["segment_name"],
                        json.dumps(segment["end_points"]),
                        str(segment["total_length"]),
                        str(segment["category"]),
                        str(segment["hidden"]),
                    ),
                )

                id_list_details.append(segment["segment_no"])
                print(f"segment_details {grand_tour} {year} uploaded")
            else:
                pass

print("JSON data uploaded successfully.")

# with open(
#    f"/Users/deniz/Projects/tdf_results/data_tools/data_cleaning/jsoniser_test_2.json",
#    "r",
# ) as f:
#
#    json_data = json.loads(f.read())
#
# id_list_json = []
# for activity in json_data:
#    if activity["activity_id"] not in id_list_json:
# cursor.execute(
#     """
#     INSERT INTO segments_json (
#         activity_id, athlete_id, date, distance, segments
#     )
#     VALUES (?, ?, ?, ?, ?)
#     """,
#     (
#         str(activity["activity_id"]),
#         str(activity["athlete_id"]),
#         str(activity["date"])
#         .replace("June", "Jun")
#         .replace("July", "Jul")
#         .replace("August", "Aug")
#         .replace("September", "Sep"),
#         float(activity["distance"]),
#         json.dumps(activity["segments"]),
#     ),
# )
#        id_list_json.append(activity["activity_id"])
#        # print(f"{j} segment {grand_tour} {year} uploaded")
#    else:
#        pass
conn.commit()
conn.close()
