import pandas as pd
import re

def clean_sites(df):
    df = df.dropna(subset=["facility"]).copy()

    # Normalize facility names
    df["facility_clean"] = (
        df["facility"]
        .fillna("Unknown")
        .str.lower()
        .str.strip()
        .str.replace(r"[\(\)\-\,]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
    )

    # Normalize country names
    df["country"] = df["country"].fillna("Unknown").str.strip().str.title()

    return df


def aggregate_site_data(df):
    def flatten_unique(series):
        flat = []
        for item in series:
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(item)
        return sorted(set(flat))

    grouped = (
        df.groupby(["facility_clean", "country"])
        .agg({
            "nct_id": lambda x: list(set(x)),  # keep full list
            "phase": flatten_unique,
            "status": flatten_unique,
            "condition": flatten_unique,
            "last_update": "max"
        })
        .reset_index()
    )

    # Add separate trial count column
    grouped["trial_count"] = grouped["nct_id"].apply(len)

    # Sort by trial count
    grouped = grouped.sort_values("trial_count", ascending=False).reset_index(drop=True)

    return grouped