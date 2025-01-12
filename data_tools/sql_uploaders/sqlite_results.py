import getpass
import sqlite3
from operator import index

import pandas as pd

from grand_tours import sql_upload

username = getpass.getuser()
data_cleaning = sql_upload.SqlUploader(
    "root", "Abrakadabra69!", "127.0.0.1", 3306, "grand_tours"
)
df = data_cleaning.clean_pro_table(
    [
        f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/pro_tdf/pro_2024_1995.csv",
    ]
)
df = df.drop_duplicates()
connection = sqlite3.connect(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/grand_tours.db"
)

df.to_sql("tdf_results", connection, if_exists="replace", index=False)
