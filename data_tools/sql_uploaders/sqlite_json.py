import getpass
import json
import re
import sqlite3
from pathlib import Path

from rich import print

from grand_tours import jsonisers, logger_config

grand_tours = ["giro", "tdf"]
years = [2013, 2014, 2015, 2016, 2017, 2018]  # 2019, 2020, 2021,2022,2023,2024]
# years = [2023]
username = getpass.getuser()

# stat_range = Path(
#    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/stats/"
# )

# details_range = Path(
#    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/mapping/"
# )

conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")
cursor = conn.cursor()
logger = logger_config.setup_logger(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.log")


try:
    with conn as connection:
        connection.execute("DROP TABLE stats_data")

    with conn as connection:
        connection.execute("DROP TABLE segments_data")

#    with conn as connection:
#        connection.execute("DROP TABLE segment_details_data")
#
#    with conn as connection:
#        connection.execute("DROP TABLE segments_json")
except sqlite3.OperationalError:
    print("Tables do not exist")

cursor.execute(
    """
CREATE TABLE segments_data (
    activity_id INTEGER PRIMARY KEY,
    athlete_id INTEGER,
    date TEXT,
    tour_year TEXT,
    distance FLOAT,
    segment BLOB
)
"""
)

cursor.execute(
    """
CREATE TABLE stats_data (
    activity_id INTEGER PRIMARY KEY,
    athlete_id INTEGER,
    tour_year TEXT,
    stat BLOB
)
"""
)

# cursor.execute(
#    """
# CREATE TABLE segment_details_data (
#    segment_id INTEGER PRIMARY KEY,
#    activity_id INTEGER,
#    segment_name TEXT,
#    category TEXT,
#    hidden TEXT,
#    end_points BLOB
# )
# """
# )
#
#
# cursor.execute(
#    """
# CREATE TABLE segments_json (
#    activity_id INTEGER PRIMARY KEY,
#    athlete_id INTEGER,
#    date TEXT,
#    distance FLOAT,
#    segments BLOB
# )
# """
# )

## Create the table in the database (if not exists)
id_list_stat = []
id_list_segment = []
id_list_details = []
for grand_tour in grand_tours:
    segment_range = Path(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/{grand_tour}_pickles")
    for year in years:
        # Define the regex pattern
        print(f"[bold yellow] ----------------{grand_tour}, {year}-------------- [/bold yellow]")
        pattern = re.compile(rf"segment_\d+_{year}_{grand_tour}\.pkl\.gz")
        # Use glob to find files and filter with regex
        matching_files = [file for file in segment_range.glob("*") if pattern.match(file.name)]
        for file in matching_files:
            json_data = json.loads(jsonisers.segment_jsoniser(file, logger))

            for activity in json_data:
                if (
                    activity["activity_id"] not in id_list_segment
                    and activity["athlete_id"] != "no id"
                    and activity["distance"] != "No distance"
                ):
                    cursor.execute(
                        """
                        INSERT INTO segments_data (
                            activity_id, athlete_id, date, tour_year, distance, segment
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            int(activity["activity_id"]),
                            int(activity["athlete_id"]),
                            str(activity["date"])
                            .replace("June", "Jun")
                            .replace("July", "Jul")
                            .replace("August", "Aug")
                            .replace("September", "Sep"),
                            str(f"{grand_tour}-{year}"),
                            float(activity["distance"]),
                            json.dumps(activity["segments"]),
                        ),
                    )
                    id_list_segment.append(activity["activity_id"])
                    # print(f"{j} segment {grand_tour} {year} uploaded")
                else:
                    pass

            json_data = json.loads(jsonisers.stat_jsoniser(file, logger))

            for activity in json_data:
                if activity["activity_id"] not in id_list_stat and activity["athlete_id"] != "no id":
                    cursor.execute(
                        """ INSERT INTO stats_data (activity_id, athlete_id, tour_year , stat) VALUES (?,?, ?, ? ) """,
                        (
                            int(activity["activity_id"]),
                            int(activity["athlete_id"]),
                            str(f"{grand_tour}-{year}"),
                            json.dumps(dict(list(activity.items())[2:])),
                        ),
                    )
                    id_list_stat.append(activity["activity_id"])
                    # print(f"{j} stats {grand_tour} {year} uploaded")
                else:
                    pass

    # for j in range(
    #    1,
    #    len(sorted(details_range.glob(f"segment_details_{year}_{grand_tour}_*")))
    #    + 1,
    # ):
    #    with open(
    # file_path = (
    #     f"/Users/{username}/iCloud/Research/Data_Science/Projects/"
    #     f"tdf_data_fin/strava/mapping/segment_details_{year}_{grand_tour}_{j}.json")
    #        "r",
    #    ) as f:
    #        json_data = json.loads(f.read())

    #    for segment in json_data:
    #        if segment["segment_no"] not in id_list_details:
    #            try:
    #                segment["category"]
    #            except KeyError:
    #                segment["category"] = None

# cursor.execute(
#     """
#     INSERT INTO segment_details_data (
#         segment_id, activity_id, segment_name, category, hidden, end_points
#     )
#     VALUES (?, ?, ?, ?, ?, ?)
#     """,
#     (
#         str(segment["segment_no"]),
#         str(segment["activity_no"]),
#         segment["segment_name"],
#         str(segment["category"]),
#         str(segment["hidden"]),
#         json.dumps(segment["end_points"]),
#     ),
# )
#            id_list_details.append(segment["segment_no"])
#            print(f"{j} segment_details {grand_tour} {year} uploaded")
#        else:
#            pass
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
