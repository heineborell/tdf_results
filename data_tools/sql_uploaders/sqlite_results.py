import getpass
import sqlite3
from pathlib import Path

import pandas as pd

from grand_tours import jsonisers, sql_upload

if __name__ == "__main__":
    username = getpass.getuser()
    path = Path("../../data/pro_tdf/")
    main_df = pd.DataFrame()
    for file in path.glob("*.pkl"):
        print(file)
        df = jsonisers.pro_csv(file)
        main_df = pd.concat([main_df, df])

    data_cleaning = sql_upload.SqlUploader(
        "root", "Abrakadabra69!", "127.0.0.1", 3306, "grand_tours"
    )

    df = data_cleaning.clean_pro_table(main_df)
    df = df.drop_duplicates()
    connection = sqlite3.connect(
        f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db"
    )

    df.to_sql("tdf_results", connection, if_exists="replace", index=False)
    df.to_csv("test.csv")
