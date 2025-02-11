import getpass
import gzip
import json
import pickle
import re

from bs4 import BeautifulSoup

username = getpass.getuser()
with gzip.open(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/tdf_pickles/segment_6119911424_2020_tdf.pkl.gz",
    "rb",
) as fp:  # Pickling
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
            i[0][2][0].split("\n")[i[0][2][0].split("\n").index("Distance") - 1]
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

# soup_list = [i[0][0] for i in data]
# Parse the HTML
# soup = BeautifulSoup((data[0][0][4]), "html.parser")

# Find all segment tables
# segment_tables = soup.select("dense.hoverable.marginless.segments") + soup.select(
#    ".dense.hidden-segments.hoverable.marginless"
# )
# print(data[2][0][4])
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
        vam_td = segment.find_all("td")[8] if len(segment.find_all("td")) > 8 else None
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
    with open(
        f"segment.json",
        "w",
    ) as f:
        f.write(json_string)
