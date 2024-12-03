from scrape import activity_scrape, ride_scrape

if __name__ == "__main__":

    pro_id = 1557033
    date = 202428
    # activity_list = ride_scrape.ride_scraper(pro_id=pro_id, date=date)
    activity_list = [
        "11888473406",
        "11888026231",
        "11888180488",
        "11888051424",
        "11879168103",
        "11878904744",
    ]
    for act in activity_list:
        print(activity_scrape.activity_scraper(act))
