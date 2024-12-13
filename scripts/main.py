from grand_tours import activity_scrape, ride_scrape

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
    activity_dict = {
        "act_id": activity_list,
        "act_date": [],
        "act_dist": [],
        "strava_id": [],
    }
    act_date = []
    act_dist = []
    strava_id = []

    for act in activity_list:
        act_date.append(activity_scrape.activity_scraper(act)[0])
        act_dist.append(activity_scrape.activity_scraper(act)[1])
        strava_id.append(activity_scrape.activity_scraper(act)[2])

    activity_dict.update(
        {"act_date": act_date, "act_dist": act_dist, "strava_id": strava_id}
    )
    print(activity_dict)
