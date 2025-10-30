import sqlite3

def save_to_db(df, db_name="trials.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("site_analysis", conn, if_exists="replace", index=False)
    conn.close()
