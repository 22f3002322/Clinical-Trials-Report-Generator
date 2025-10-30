import pandas as pd

def clean_sites(df):
    df = df.dropna(subset=["facility"])
    df["facility_clean"] = df["facility"].str.strip().str.lower()
    df["country"] = df["country"].fillna("Unknown")
    return df

def aggregate_site_data(df):
    df["facility_clean"] = df["facility"].fillna("Unknown").str.strip()

    def flatten_unique(series):
        flat = []
        for item in series:
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(item)
        return list(set(flat))

    grouped = df.groupby(["facility_clean", "country"]).agg({
        "nct_id": "nunique",
        "phase": flatten_unique,
        "status": flatten_unique,
        "condition": flatten_unique,   # ✅ ADDED THIS LINE
        "last_update": "max"
    }).reset_index()

    grouped.rename(columns={
        "nct_id": "trial_count",
    }, inplace=True)

    return grouped