import getpass

import pandas as pd
from sqlalchemy import create_engine

from grand_tours import segment_scraper

# grand_tour = "giro"
grand_tour = "tdf"
year = 2013


activity_no_list = (
    pd.read_csv(
        f"~/iCloud/Research/Data_Science/Projects/data/strava/activity_list/activity_list_{grand_tour}_{year}.csv"
    )
    .drop_duplicates(subset=["activity"])["activity"]
    .values.tolist()
)

# last_index = activity_no_list.index("9406303142")
# activity_no_list = activity_no_list[:12]
print(len(activity_no_list))

scraper = segment_scraper.SegmentScrape(grand_tour, year, activity_no_list, 1)
scraper.segment_scraper()
