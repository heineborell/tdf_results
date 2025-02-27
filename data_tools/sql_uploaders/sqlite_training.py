import getpass
import json
import re
import sqlite3
from pathlib import Path

from rich import print

from grand_tours import jsonisers, logger_config

if __name__ == "__main__":
    username = getpass.getuser()
    # grand_tour = "vuelta"
    grand_tour = "tdf"

    grand_tours = ["tdf_training"]
    years = [2024]
    username = getpass.getuser()

    conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/training.db")
    cursor = conn.cursor()
    logger = logger_config.setup_logger(
        f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/{grand_tour}.log"
    )
    try:
        with conn as connection:
            connection.execute("DROP TABLE stats_data")

        with conn as connection:
            connection.execute("DROP TABLE segments_data")

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

    ## Create the table in the database (if not exists)
    id_list_stat = []
    id_list_segment = []
    id_list_details = []
    for grand_tour in grand_tours:
        segment_range = Path(
            f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/{grand_tour}_pickles"
        )
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
                                activity["date"]
                                .replace("June", "Jun")
                                .replace("July", "Jul")
                                .replace("August", "Aug")
                                .replace("September", "Sep"),
                                f"{grand_tour}-{year}",
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
                            """
                            INSERT INTO stats_data (activity_id, athlete_id, tour_year, stat)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                int(activity["activity_id"]),
                                int(activity["athlete_id"]),
                                f"{grand_tour}-{year}",
                                json.dumps(dict(list(activity.items())[2:])),
                            ),
                        )
                        id_list_stat.append(activity["activity_id"])
                        # print(f"{j} stats {grand_tour} {year} uploaded")
                    else:
                        pass

    print("JSON data uploaded successfully.")
    conn.commit()
    conn.close()
