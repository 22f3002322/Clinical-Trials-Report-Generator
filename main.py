from extract import fetch_trials
from transform import clean_sites, aggregate_site_data
from score import compute_match_score, compute_data_quality
from database import save_to_db
from analyze import summarize_sites

# 1️⃣ Extract
df = fetch_trials(condition="lung cancer", phase="Phase 3", max_results=200)

# 2️⃣ Transform
df = clean_sites(df)
sites = aggregate_site_data(df)

# 3️⃣ Compute Scores
sites["match_score"] = sites.apply(lambda x: compute_match_score(x, "lung cancer", "Phase 3", "India"), axis=1)
sites["data_quality"] = sites.apply(compute_data_quality, axis=1)

# 4️⃣ Save and Analyze
save_to_db(sites)
summary = summarize_sites(sites)
print(summary.head())
