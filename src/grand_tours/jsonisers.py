import gzip
import json
import pickle
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import except_


def pro_csv(path, logger):
    with open(path, "rb") as fp:  # Pickling
        data = pickle.load(fp)

    final_dict = {}
    df = pd.DataFrame()
    for i in range(len(data)):
        if (
            len(data[i][0])
            == len(data[i][1])
            == len(data[i][2][0])
            == len(data[i][2][1])
        ):
            final_dict.update(
                {
                    "year": data[i][0],
                    "stage": data[i][1],
                    "name": data[i][2][0],
                    "time": data[i][2][1],
                }
            )
            info_lst = data[i][2][2]
            final_info_lst = []
            for j in info_lst:
                if len(j.split("\n")) == 1:
                    single_el = j.split("\n")
                    single_el.append("Na")
                    final_info_lst.append(single_el)
                else:
                    final_info_lst.append(j.split("\n"))

            final_info_lst = np.array(final_info_lst).flatten()

            # construct info table dictionary
            info_dict = dict(zip(final_info_lst[0::2], final_info_lst[1::2]))
            info_dict = {
                key: [value] * len(data[i][0]) for key, value in info_dict.items()
            }
            df_joined = pd.concat(
                [pd.DataFrame.from_dict(final_dict), pd.DataFrame.from_dict(info_dict)],
                axis=1,
            )

            df = pd.concat([df, df_joined])
        else:
            try:
                logger.info(
                    f"{data[i][0][0], data[i][1][0]}, ---------the index lengths are not same."
                )
            except IndexError:
                logger.info(f"{data[i]}, ------ that is problematic")
    return df


def segment_jsoniser(filepath):
    with gzip.open(filepath, "rb") as fp:  # Pickling
        data = pickle.load(fp)

    activity_id_list = [i[0][0][0] for i in data]
    activity_type_list = [i[0][1][0] for i in data]

    athelete_id_list = []
    for key, value in enumerate(data):
        try:
            athelete_id_list.append(value[0][3][0])
        except IndexError:
            athelete_id_list.append("no id")
            print("No athelete id", key)

    date_list = []
    for key, value in enumerate(data):
        try:
            pattern = r"\b([A-Z][a-z]+) (\d{1,2}) (\d{4})\b"
            matching = re.findall(
                pattern,
                (value[0][2][0].split(",")[1]).strip()
                + " "
                + (value[0][2][0].split(",")[2].split(" ")[1]).strip(),
            )
            date_list.append(f"{matching[0][0]} {matching[0][1]} {matching[0][2]}")
        except IndexError:
            date_list.append("No date")
            print("no date", key)

    distance_list = []
    for i in data:
        try:
            distance_list.append(
                float(
                    re.search(
                        r"\d+(\.\d+)?",
                        i[0][2][0].split("\n")[
                            i[0][2][0].split("\n").index("Distance") - 1
                        ],
                    ).group()
                )
            )
        except (ValueError, IndexError):
            distance_list.append("No distance")

    activity_dict_list = [{"activity_id": i} for i in activity_id_list]

    for i, no in enumerate(activity_dict_list):
        no = no.update({"athlete_id": athelete_id_list[i]})

    for i, no in enumerate(activity_dict_list):
        no = no.update({"activity_type": activity_type_list[i]})

    for i, no in enumerate(activity_dict_list):
        no = no.update({"date": date_list[i]})

    for i, no in enumerate(activity_dict_list):
        no = no.update({"distance": distance_list[i]})

    for key, element in enumerate(data):
        try:
            segment_table = BeautifulSoup(element[0][4][0], "html.parser")
        except IndexError:
            segment_table = BeautifulSoup("None", "html.parser")
        # Initialize empty dictionary
        segment_dict = {}

        segment_no = []
        segment_name = []
        segment_distance = []
        segment_vert = []
        segment_grade = []
        segment_time = []
        segment_speed = []
        watt = []
        heart_rate = []
        VAM = []

        for m, segment in enumerate(segment_table.find_all("tr")):
            if m == 0:
                continue  # Skip the first row (header)

            # An example of the html structure that is scraped
            # <td class="name-col">
            # <div class="name">
            #    Manson Charada DD
            #  </div>
            # <div class="stats">
            # <span title="Distance">
            #      0.78<abbr class="unit" title="kilometers"> km</abbr>
            # </span>
            # <span title="Elevation difference">
            #      32<abbr class="unit" title="meters"> m</abbr>
            # </span>
            # <span title="Average grade">
            #      -3.7<abbr class="unit" title="percent">%</abbr>
            # </span>
            # </div>
            # <div class="segment-effort-detail">
            # <div class="content"></div>
            # </div>
            # </td>

            # Get segment effort ID
            segment_no.append(segment.get("data-segment-effort-id", "N/A"))

            name_td = segment.find("td", class_="name-col")
            if name_td:
                # Extract the full text content inside <td>
                full_text = name_td.get_text(separator=" | ", strip=True)

                # Extract specific elements
                name = (
                    name_td.find("div", class_="name").get_text(strip=True)
                    if name_td.find("div", class_="name")
                    else "N/A"
                )
                segment_name.append(name)

                stats_div = name_td.find("div", class_="stats")
                if stats_div:
                    stats_text = stats_div.get_text(separator=" | ", strip=True)
                else:
                    stats_text = "N/A"

                # Extract individual stats
                distance = (
                    stats_div.find("span", {"title": "Distance"})
                    .get_text(strip=True)
                    .replace("\n", " ")
                    if stats_div
                    else "N/A"
                )
                segment_distance.append(distance)
                elevation = (
                    stats_div.find("span", {"title": "Elevation difference"})
                    .get_text(strip=True)
                    .replace("\n", " ")
                    if stats_div
                    else "N/A"
                )
                segment_vert.append(elevation)
                grade = (
                    stats_div.find("span", {"title": "Average grade"})
                    .get_text(strip=True)
                    .replace("\n", " ")
                    if stats_div
                    else "N/A"
                )
                segment_grade.append(grade)
            else:
                segment_dict = {}

            # An example of the html structure that is scraped
            # <td class="climb-cat-col"><span class="icon-cat-4 strava-icon" title="Category 4 Climb"></span></td>
            # <td class="time-col">3:47</td>
            # <td>
            #  13.3<abbr class="unit" title="kilometers per hour"> km/h</abbr>
            # </td>
            # <td>
            #  297<abbr class="unit" title="watts"> W</abbr>
            # </td>
            # <td>1846</td>
            # <td>
            #  137<abbr class="unit" title="beats per minute">bpm</abbr></td>
            # <td>

            # Extract Climb Category
            climb_td = segment.find("td", class_="climb-cat-col")
            climb_category = climb_td.text.strip() if climb_td else "N/A"

            # Extract Time
            time_td = segment.find("td", class_="time-col")
            segment_time.append(time_td.get_text(strip=True) if time_td else "N/A")

            # Extract Speed
            speed_td = segment.find_all("td")[6]  # Speed is in the 5th <td> (index 4)
            segment_speed.append(speed_td.get_text(strip=True) if speed_td else "N/A")

            # Extract Watts
            watts_td = segment.find_all("td")[7]  # Watts is in the 6th <td> (index 5)
            watt.append(watts_td.get_text(strip=True) if watts_td else "N/A")

            # Extract VAM (optional, may not exist)
            vam_td = (
                segment.find_all("td")[8] if len(segment.find_all("td")) > 8 else None
            )
            VAM.append(vam_td.get_text(strip=True) if vam_td else "N/A")

            # Extract Heart Rate
            heart_rate_td = (
                segment.find_all("td")[9] if len(segment.find_all("td")) > 9 else None
            )
            heart_rate.append(
                heart_rate_td.get_text(strip=True) if heart_rate_td else "N/A"
            )

            ## Assign extracted data to the dictionary
            segment_dict = {
                # "segment_no": segment_no,
                # 'climb_category': climb_category,
                "segment_name": segment_name,
                "segment_time": segment_time,
                "segment_speed": segment_speed,
                "watt": watt,
                "heart_rate": heart_rate,
                "segment_distance": segment_distance,
                "segment_vert": segment_vert,
                "segment_grade": segment_grade,
                "VAM": VAM,
            }
        activity_dict_list[key].update({"segments": segment_dict})

        json_string = json.dumps(activity_dict_list)

    return json_string


def stat_jsoniser(filepath):
    with gzip.open(filepath, "rb") as fp:  # Pickling
        data = pickle.load(fp)

    activity_id_list = [i[0][0][0] for i in data]
    activity_type_list = [i[0][1][0] for i in data]

    athelete_id_list = []
    for key, value in enumerate(data):
        try:
            athelete_id_list.append(value[0][3][0])
        except IndexError:
            athelete_id_list.append("no id")
            print("No athelete id", key)

    date_list = []
    for key, value in enumerate(data):
        try:
            pattern = r"\b([A-Z][a-z]+) (\d{1,2}) (\d{4})\b"
            matching = re.findall(
                pattern,
                (value[0][2][0].split(",")[1]).strip()
                + " "
                + (value[0][2][0].split(",")[2].split(" ")[1]).strip(),
            )
            date_list.append(f"{matching[0][0]} {matching[0][1]} {matching[0][2]}")
        except IndexError:
            date_list.append("No date")
            print("no date", key)

    distance_list = []
    for i in data:
        try:
            distance_list.append(
                float(
                    re.search(
                        r"\d+(\.\d+)?",
                        i[0][2][0].split("\n")[
                            i[0][2][0].split("\n").index("Distance") - 1
                        ],
                    ).group()
                )
            )
        except (ValueError, IndexError):
            distance_list.append("No distance")

    stat_dict_list = []

    for i, no in enumerate(stat_dict_list):
        no = no.update({"athlete_id": athelete_id_list[i]})

    stat_list = [i[0][-1] for i in data]
    for p, stats in enumerate(stat_list):
        stat_dict = {}
        stat_dict.update(
            {
                "activity_id": activity_id_list[p],
                "athlete_id": athelete_id_list[p],
            }
        )
        try:
            stats.remove("Show More")
        except ValueError:
            print("No more stat", p)

        for i, stat in enumerate(stats):
            if stat == "Distance":
                stat_dict.update(
                    {
                        "dist": stats[i - 1],
                    }
                )
            if stat == "Moving Time":
                stat_dict.update({"move_time": stats[i - 1]})
            if stat == "Elevation":
                stat_dict.update({"elevation": stats[i - 1]})
            if stat == "Weighted Avg Power":
                stat_dict.update({"wap": stats[i - 1]})
            if stat == "total work":
                stat_dict.update({"tw": stats[i - 1]})
            if stat == "Avg Max":
                stat_dict.update({"avg_max": stats[i + 1]})
            if "Elapsed Time" in stat:
                stat_dict.update({"elapsed": stats[i].split(" ")[-1]})
            if stat == "Temperature":
                stat_dict.update({"temp": stats[i + 1]})
            if stat == "Humidity":
                stat_dict.update({"humd": stats[i + 1]})
            if stat == "Feels like":
                stat_dict.update({"feels": stats[i + 1]})
            if stat == "Wind Speed":
                stat_dict.update({"wind_speed": stats[i + 1]})
            if stat == "Wind Direction":
                stat_dict.update({"wind_direction": stats[i + 1]})
            if i == len(stats) - 1:
                stat_dict.update({"device": stats[i]})

        stat_dict_list.append(stat_dict)

        json_string = json.dumps(stat_dict_list)

    return json_string
