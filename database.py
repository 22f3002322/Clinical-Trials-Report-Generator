import sqlite3
import pandas as pd

DB_PATH = "clinical_trials.db"

# =========================================
# 🔹 Save main trial site data
# =========================================
def save_to_db(df, db_path=DB_PATH):
    # Convert list columns to comma-separated strings before saving
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: ", ".join(map(str, x)) if isinstance(x, list) else x)

    conn = sqlite3.connect(db_path)
    df.to_sql("site_analysis", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Data successfully saved to {db_path}")


# =========================================
# 🔹 Save metadata about last fetch
# =========================================
def save_metadata(condition, phase, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition TEXT,
            phase TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert new metadata record
    cur.execute(
        "INSERT INTO metadata (condition, phase) VALUES (?, ?)",
        (condition, phase)
    )

    conn.commit()
    conn.close()
    print(f"🧠 Metadata saved — condition: '{condition}', phase: '{phase}'")


# =========================================
# 🔹 Load latest metadata (for Streamlit app)
# =========================================
def load_latest_metadata(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # ✅ Ensure the metadata table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition TEXT,
            phase TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        SELECT condition, phase, updated_at 
        FROM metadata 
        ORDER BY updated_at DESC 
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    if row:
        return {"condition": row[0], "phase": row[1], "updated_at": row[2]}
    return None

# =========================================
# 🔹 (Optional) Load data from DB
# =========================================
def load_from_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM site_analysis", conn)
    conn.close()
    return df
