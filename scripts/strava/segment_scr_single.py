import pandas as pd

from grand_tours import getters, segment_scraper

if __name__ == "__main__":
    # grand_tour = "giro"
    grand_tour = "tdf"
    year = 2017

    activity_no_list = (
        pd.read_csv(
            f"~/iCloud/Research/Data_Science/Projects/data/strava/activity_list/activity_list_{grand_tour}_{year}.csv"
        )
        .drop_duplicates(subset=["activity"])["activity"]
        .values.tolist()
    )
    # Turn to this on for removing duplicates

    print(len(activity_no_list))
    duplicate_list = getters.get_duplicates(year, grand_tour)
    activity_no_list = [i for i in activity_no_list if i not in duplicate_list]

    # last_index = activity_no_list.index("9406303142")
    # activity_no_list = activity_no_list[:12]
    print(len(activity_no_list))

    scraper = segment_scraper.SegmentScrape(grand_tour, year, activity_no_list, 1)
    scraper.segment_scraper()
