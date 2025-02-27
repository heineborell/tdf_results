import getpass

import pandas as pd
from rich import print

from grand_tours import getters, segment_scraper

if __name__ == "__main__":
    grand_tour = "tdf_training"
    year = 2023
    username = getpass.getuser()

    activity_no_list = (
        pd.read_csv(
            f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/training_list/{grand_tour}_{year}.csv"
        )
        .drop_duplicates(subset=["activity_id"])["activity_id"]
        .values.tolist()
    )
    # Turn to this on for removing duplicates

    print(len(activity_no_list))
    duplicate_list = getters.get_duplicates(year, grand_tour, username)
    activity_no_list = [i for i in activity_no_list if i not in duplicate_list]

    print(len(activity_no_list))

    scraper = segment_scraper.SegmentScrape(username, grand_tour, year, activity_no_list, 2)
    scraper.segment_scraper()
