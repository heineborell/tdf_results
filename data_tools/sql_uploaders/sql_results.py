from sqlalchemy.types import *

from grand_tours import sql_upload

test1 = sql_upload.SqlUploader(
    "root", "Abrakadabra69!", "127.0.0.1", 3306, "grand_tours"
)
test1.create_db()
test1.clean_pro_table(
    [
        "~/iCloud/Research/Data_Science/Projects/data/pro_giro/pro_2024_1991_edt.csv",
        "~/iCloud/Research/Data_Science/Projects/data/pro_giro/pro_1991_1933.csv",
        "~/iCloud/Research/Data_Science/Projects/data/pro_giro/pro_1933_1923.csv",
    ]
)

df_schema = {
    "name": String(64),
    "year": Integer,
    "time": Integer,
    "profile_score": Integer,
    "vertical_meters": Integer,
}
test1.csv_uploader(df_schema=df_schema, table_name="giro_results")

test1.clean_pro_table(
    [
        "~/iCloud/Research/Data_Science/Projects/data/pro_tdf/pro_1919_1903.csv",
        "~/iCloud/Research/Data_Science/Projects/data/pro_tdf/pro_1995_1919.csv",
        "~/iCloud/Research/Data_Science/Projects/data/pro_tdf/pro_2024_1995.csv",
    ]
)

test1.csv_uploader(df_schema=df_schema, table_name="tdf_results")
