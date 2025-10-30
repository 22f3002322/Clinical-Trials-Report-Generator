def compute_match_score(row, target_condition, target_phase, target_country):
    condition_values = row.get("condition", [])
    if isinstance(condition_values, str):
        condition_values = [condition_values]
    condition_text = ",".join(condition_values).lower()

    condition_match = int(target_condition.lower() in condition_text)
    phase_match = int(any(target_phase.lower() in str(p).lower() for p in row.get("phase", [])))
    country_match = int(target_country.lower() == str(row.get("country", "")).lower())

    return (condition_match * 0.5) + (phase_match * 0.3) + (country_match * 0.2)


def compute_data_quality(row):
    completeness = 1 if row["last_update"] else 0.8
    recency = 1.0 if row["last_update"] and int(row["last_update"][:4]) >= 2023 else 0.7
    return round(0.5*completeness + 0.5*recency, 2)
