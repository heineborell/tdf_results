import sqlite3

# Paths for databases
old_db_path = "/Users/deniz/iCloud/Research/Data_Science/Projects/data/training.db"  # Existing database (DO NOT MODIFY)
new_db_path = "/Users/deniz/iCloud/Research/Data_Science/Projects/data/training_merged.db"  # New database

# SQL Queries
create_table_query = """
CREATE TABLE IF NOT EXISTS training_table (
    activity_id INTEGER,
    athlete_id INTEGER,
    tour_year TEXT,
    date TEXT,
    stat BLOB,
    segment BLOB
);
"""

select_data_query = """
SELECT t1.activity_id, t1.athlete_id, t2.tour_year, t1.date, t2.stat, t1.segment
FROM segments_data AS t1
LEFT JOIN stats_data AS t2
ON t1.activity_id = t2.activity_id;
"""

# Connect to old and new databases
with sqlite3.connect(old_db_path) as old_conn, sqlite3.connect(new_db_path) as new_conn:
    old_cursor = old_conn.cursor()
    new_cursor = new_conn.cursor()

    # Drop training_table if it exists
    try:
        new_cursor.execute("DROP TABLE training_table")
        print("training_table droppped.")

    except sqlite3.OperationalError:
        print("Tables do not exist")

    # Create the table in the new database
    new_cursor.execute(create_table_query)

    # Fetch data from old database
    old_cursor.execute(select_data_query)
    data = old_cursor.fetchall()

    # Insert data into the new database
    new_cursor.executemany("INSERT INTO training_table VALUES (?, ?, ?, ?, ?, ?)", data)

    # Commit changes
    new_conn.commit()

print("New database 'training_db.db' created with only 'training_table'. Old tables removed.")
