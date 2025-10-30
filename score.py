def compute_match_score(row, target_condition, target_phase, target_country):
    condition_match = int(target_condition.lower() in ",".join(row["condition"]).lower())
    phase_match = int(target_phase in row["phase"])
    region_match = int(target_country.lower() == row["country"].lower())
    return 0.5*condition_match + 0.3*phase_match + 0.2*region_match

def compute_data_quality(row):
    completeness = 1 if row["last_update"] else 0.8
    recency = 1.0 if row["last_update"] and int(row["last_update"][:4]) >= 2023 else 0.7
    return round(0.5*completeness + 0.5*recency, 2)
