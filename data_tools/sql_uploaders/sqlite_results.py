import getpass
import os
import sqlite3
from pathlib import Path

import pandas as pd

from grand_tours import jsonisers, sql_upload
from grand_tours.logger_config import setup_logger

if __name__ == "__main__":
    username = getpass.getuser()
    grand_tour = "vuelta"
    # grand_tour = "tdf"
    path = Path(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/pro_{grand_tour}")
    main_df = pd.DataFrame()
    logger = setup_logger(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/{grand_tour}.log")
    for file in path.glob("*.pkl"):
        df = jsonisers.pro_csv(file, logger)
        main_df = pd.concat([main_df, df])

    data_cleaning = sql_upload.SqlUploader(
        os.getenv("mysql_user"),
        os.getenv("mysql_password"),
        os.getenv("mysql_host"),
        os.getenv("mysql_port"),
        os.getenv("mysql_database"),
    )

    df = data_cleaning.clean_pro_table(main_df)
    df = df.drop_duplicates()
    connection = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")

    df.to_sql(f"{grand_tour}_results", connection, if_exists="replace", index=False)
