import gzip
import pickle

import numpy as np
import pandas as pd

with gzip.open(
    f"../../scripts/strava/segment_6151368704_2013_tdf.pkl.gz", "rb"
) as fp:  # Pickling
    data = pickle.load(fp)


activity_id_list = [i[0][0][0] for i in data]
activity_type_list = [i[0][1][0] for i in data]
athelete_id_list = [i[0][3][0] for i in data]
date_list = [
    (i[0][2][0].split(",")[1]) + " " + (i[0][2][0].split(",")[2].split(" ")[1])
    for i in data
]
activity_dict_list = [{"activity_id": i} for i in activity_id_list]

for i, no in enumerate(activity_dict_list):
    no = no.update({"athlete_id": athelete_id_list[i]})

for i, no in enumerate(activity_dict_list):
    no = no.update({"activity_type": activity_type_list[i]})

for i, no in enumerate(activity_dict_list):
    no = no.update({"date": date_list[i]})

#    try:
#        distance = summary_container.text.split("\n")[
#            summary_container.text.split("\n").index("Distance") - 1
#        ].split(" ")[0]
#    except ValueError:
#        print("No Distance")

print(activity_dict_list)
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
activity_dict = {
    #    "activity_id": activity_no,
    #        "athlete_id": name,
    #        "date": date,
    #        "distance": distance,
    #        "segments": [],
}
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
