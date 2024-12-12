from sqlalchemy.types import *

from scrape import sql_upload

test1 = sql_upload.SqlUploader("root", "Abrakadabra69!", "127.0.0.1", 3306, "test_db")
test1.clean_pro_table(["../data/pro_cycling_db/pro_tdf/protdf_giro_2024_2008.csv"])

df_schema = {
    "name": String(64),
    "year": Integer,
    "time": Integer,
    "profile_score": Integer,
    "vertical_meters": Integer,
}
test1.csv_uploader(df_schema=df_schema, table_name="giro_results")
