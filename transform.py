import pandas as pd

def clean_sites(df):
    df = df.dropna(subset=["facility"])
    df["facility_clean"] = df["facility"].str.strip().str.lower()
    df["country"] = df["country"].fillna("Unknown")
    return df

def aggregate_site_data(df):
    grouped = df.groupby(["facility_clean", "country"]).agg({
        "nct_id": "count",
        "status": lambda x: x.value_counts().to_dict(),
        "phase": lambda x: list(set(x)),
        "condition": lambda x: list(set(x)),
        "last_update": "max"
    }).reset_index()

    grouped.rename(columns={"nct_id": "total_studies"}, inplace=True)
    return grouped
score.py