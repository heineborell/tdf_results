from scrape import activity_scrape, ride_scrape

if __name__ == "__main__":

    pro_id = 1557033
    date = 202428
    activity_list = ride_scrape.ride_scraper(pro_id=pro_id, date=date)
    print(activity_list)
