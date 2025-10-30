import pandas as pd

def summarize_sites(df):
    df["completed_rate"] = df["status"].apply(lambda x: x.get("Completed", 0) / sum(x.values()) if isinstance(x, dict) else 0)
    summary = df.sort_values(by="completed_rate", ascending=False)
    return summary[["facility_clean", "country", "total_studies", "completed_rate", "last_update"]]
