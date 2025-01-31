import getpass
import gzip
import json
import pickle
import re

from bs4 import BeautifulSoup

username = getpass.getuser()
with gzip.open(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/tdf_pickles/segment_6175322112_2018_tdf.pkl.gz",
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

        # with open(
        #    f"inner_2.txt",
        #    "w",
        # ) as f:
        #    try:
        #        f.write(element[0][4][0])
        #    except IndexError:
        #        pass

# if len(fields) > 5:
#    segment_time.append(fields[5].get_text())

# if len(fields) > 6:
#    segment_speed.append(fields[6].get_text().split(" ")[0])

# if len(fields) > 7:
#    watt.append(fields[7].get_text().split(" ")[0])

# if len(fields) > 8:
#    VAM.append(fields[8].get_text())

# if len(fields) > 9:
#    heart_rate.append(fields[9].get_text().split("b")[0])

## Assign extracted data to the dictionary
# segment_dict = {
#    "segment_no": segment_no,
#    "segment_name": segment_name,
#    "segment_time": segment_time,
#    "segment_speed": segment_speed,
#    "watt": watt,
#    "heart_rate": heart_rate,
#    "segment_distance": segment_distance,
#    "segment_vert": segment_vert,
#    "segment_grade": segment_grade,
#    "VAM": VAM,
# }

# Print the result
# print(segment_dict)
# stat_dict_list = []

# for p, activity_no in enumerate(activity_no_list):
#
#
#    # Get text content and parse activity_type
#    script_text = script_element.get_attribute("innerHTML")
#    activity_type = script_text.split('activity_type":"')[1].split('"')[0]
#    print(activity_type)
#
#    # Check if the activity type is 'Ride'
#    if activity_type == "ride":
#        print("Found ride activity type!")
#    else:
#        print("Ride activity type not found.")
#        continue
#
#    summary_container = driver.find_element(
#        By.CSS_SELECTOR, ".row.no-margins.activity-summary-container"
#    )
#    summary_pre = summary_container.text.split("\n")[0].split(",")
#    date = summary_pre[1] + " " + summary_pre[2].split(" ")[1]
#    date = date.strip()
#    try:
#        distance = summary_container.text.split("\n")[
#            summary_container.text.split("\n").index("Distance") - 1
#        ].split(" ")[0]
#    except ValueError:
#        print("No Distance")
#
#    for i in driver.find_elements(By.XPATH, "//*[@id='heading']/header/h2/span/a"):
#        name = i.get_attribute("href").split("/")[-1]
#
#
#    try:
#        driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]')[0].click()
#        segment_table = driver.find_element(
#            By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
#        )
#        segment_tables = driver.find_elements(
#            By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
#        )
#        segment_tables.append(
#            driver.find_element(
#                By.CSS_SELECTOR, ".dense.hidden-segments.hoverable.marginless"
#            )
#        )
#    except NoSuchElementException:
#        print("no segments")
#
#    else:
#        print(activity_no, p)
#        segment_no = []
#        segment_name = []
#        segment_distance = []
#        segment_vert = []
#        segment_grade = []
#        segment_time = []
#        segment_speed = []
#        watt = []
#        heart_rate = []
#        VAM = []
#        for g, segment_table in enumerate(segment_tables):
#            for m, segment in enumerate(segment_table.find_elements(By.TAG_NAME, "tr")):
#                if m == 0 and g == 0:
#                    pass
#                else:
#                    segment_no.append(segment.get_attribute("data-segment-effort-id"))
#                for i, field in enumerate(segment.find_elements(By.TAG_NAME, "td")):
#                    if i == 3:
#                        segment_name.append(field.text.split("\n")[0])
#                        segment_distance.append(field.text.split("\n")[1].split(" ")[0])
#                        segment_vert.append(field.text.split("\n")[1].split(" ")[2])
#                        segment_grade.append(
#                            field.text.split("\n")[1].split(" ")[4].split("%")[0]
#                        )
#                    elif i == 5:
#                        segment_time.append(field.text)
#                    elif i == 6:
#                        segment_speed.append(field.text.split(" ")[0])
#                    elif i == 7:
#                        watt.append(field.text.split(" ")[0])
#                    elif i == 8:
#                        VAM.append(field.text)
#                    elif i == 9:
#                        heart_rate.append(field.text.split("b")[0])
#
#        segment_dict = {
#            "segment_no": segment_no,
#            "segment_name": segment_name,
#            "segment_time": segment_time,
#            "segment_speed": segment_speed,
#            "watt": watt,
#            "heart_rate": heart_rate,
#            "segment_distance": segment_distance,
#            "segment_vert": segment_vert,
#            "segment_grade": segment_grade,
#            "VAM": VAM,
#        }
#        # activity_dict["activities"][0]['activity_id'].append(activity_no)
#        activity_dict["segments"].append(segment_dict)
#        activity_dict_list["activities"].append(activity_dict)
#
#        try:
#            stats = driver.find_element(By.XPATH, '//*[@id="heading"]/div/div/div[2]')
#            stat_list = stats.text.split("\n")
#            stat_list.remove("Show More")
#            stat_dict = {}
#            for i, stat in enumerate(stat_list):
#                if stat == "Distance":
#                    stat_dict.update(
#                        {
#                            "activity_id": activity_no,
#                            "athlete_id": name,
#                            "dist": stat_list[i - 1],
#                        }
#                    )
#                if stat == "Moving Time":
#                    stat_dict.update({"move_time": stat_list[i - 1]})
#                if stat == "Elevation":
#                    stat_dict.update({"elevation": stat_list[i - 1]})
#                if stat == "Weighted Avg Power":
#                    stat_dict.update({"wap": stat_list[i - 1]})
#                if stat == "total work":
#                    stat_dict.update({"tw": stat_list[i - 1]})
#                if stat == "Avg Max":
#                    stat_dict.update({"avg_max": stat_list[i + 1]})
#                if "Elapsed Time" in stat:
#                    stat_dict.update({"elapsed": stat_list[i].split(" ")[-1]})
#                if stat == "Temperature":
#                    stat_dict.update({"temp": stat_list[i + 1]})
#                if stat == "Humidity":
#                    stat_dict.update({"humd": stat_list[i + 1]})
#                if stat == "Feels like":
#                    stat_dict.update({"feels": stat_list[i + 1]})
#                if stat == "Wind Speed":
#                    stat_dict.update({"wind_speed": stat_list[i + 1]})
#                if stat == "Wind Direction":
#                    stat_dict.update({"wind_direction": stat_list[i + 1]})
#                if i == len(stat_list) - 1:
#                    stat_dict.update({"device": stat_list[i]})
#
#            stat_dict_list["stats"].append(stat_dict)
#            print(stat_dict)
#        except ValueError:
#            print("No more stat")
#
#        json_string = json.dumps(activity_dict_list)
#        with open(
#            f"segment_{year}_{grand_tour}.json",
#            "w",
#        ) as f:
#            f.write(json_string)
#        json_string = json.dumps(stat_dict_list)
#        with open(
#            f"stat_{year}_{grand_tour}.json",
#            "w",
#        ) as f:
#            f.write(json_string)
#    time.sleep(3)
#
#
# driver.quit()
