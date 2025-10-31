import argparse
from extract import fetch_trials
from transform import clean_sites, aggregate_site_data
from score import compute_match_score, compute_data_quality
from database import save_to_db, save_metadata
from analyze import summarize_sites

def main(condition, phase, max_results=1000):
    print(f"\n🚀 Running pipeline for condition='{condition}', phase='{phase}'")

    # 1️⃣ Extract
    df = fetch_trials(condition=condition, phase=phase, max_results=max_results)

    # 2️⃣ Transform
    df = clean_sites(df)
    sites = aggregate_site_data(df)

    # 3️⃣ Compute Scores
    sites["match_score"] = sites.apply(
        lambda x: compute_match_score(x, condition, f"Phase {phase}", "India"), axis=1
    )
    sites["data_quality"] = sites.apply(compute_data_quality, axis=1)

    # 4️⃣ Save and Analyze
    save_to_db(sites)
    summary = summarize_sites(sites)
    summary.to_csv("clinical_summary.csv", index=False)
    print("✅ Saved summary to clinical_summary.csv")

    # 5️⃣ Save metadata
    save_metadata(condition, phase)
    print(f"✅ Metadata saved: condition='{condition}', phase='{phase}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clinical Trials Data Pipeline")
    parser.add_argument("--condition", type=str, required=True, help="Medical condition (e.g., lung cancer)")
    parser.add_argument("--phase", type=str, required=True, help="Trial phase (1, 2, or 3)")
    parser.add_argument("--max_results", type=int, default=1000, help="Max results to fetch")
    args = parser.parse_args()

    main(args.condition, args.phase, args.max_results)
