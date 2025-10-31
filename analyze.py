import pandas as pd

def summarize_sites(df):
    # Defensive copy
    summary = df.copy()

    # Define only the columns that actually exist
    agg_dict = {
        "trial_count": "sum",
        "match_score": "mean" if "match_score" in df.columns else "first",
        "data_quality": "mean" if "data_quality" in df.columns else "first",
        "last_update": "max"
    }

    # Only include completed_rate if it exists
    if "completed_rate" in df.columns:
        agg_dict["completed_rate"] = "mean"

    summary = summary.groupby(["facility_clean", "country"], as_index=False).agg(agg_dict)

    return summary
