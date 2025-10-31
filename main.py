from extract import fetch_trials
from transform import clean_sites, aggregate_site_data
from score import compute_match_score, compute_data_quality
from database import save_to_db
from analyze import summarize_sites

# 1️⃣ Extract
df = fetch_trials(condition="cancer", phase="3", max_results=1000)
print(f"\n✅ Raw trials fetched: {len(df)}")
print(df.head(3))

# 2️⃣ Transform
df = clean_sites(df)

print("\n🔍 Sample facilities before grouping:")
print(df["facility_clean"].value_counts().head(20))

dupes = df[df.duplicated(subset=["nct_id", "facility_clean", "country"], keep=False)]
print(f"\n📊 Duplicates for same trial+facility: {len(dupes)}")

sites = aggregate_site_data(df)
print("\n🏥 Aggregated Site Summary:")
print(sites.head(10))

# 3️⃣ Compute Scores
print("\n⚙️ Computing match scores & data quality metrics...")
sites["match_score"] = sites.apply(
    lambda x: compute_match_score(x, "lung cancer", "Phase 3", "India"), axis=1
)
sites["data_quality"] = sites.apply(compute_data_quality, axis=1)

# 4️⃣ Save and Analyze
print("\n💾 Saving to database...")
save_to_db(sites)

print("\n📈 Generating site summary...")
summary = summarize_sites(sites)
print(summary.head())

summary.to_csv("clinical_summary.csv", index=False)
print("\n✅ clinical_summary.csv saved successfully!")
