import sqlite3
import pandas as pd

def save_to_db(df, db_path="clinical_trials.db"):
    # Convert list columns to comma-separated strings
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: ", ".join(map(str, x)) if isinstance(x, list) else x)

    conn = sqlite3.connect(db_path)
    df.to_sql("site_analysis", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Data successfully saved to {db_path}")
