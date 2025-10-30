import requests
import pandas as pd

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def fetch_trials(condition=None, phase=None, max_results=100):
    """
    Fetches clinical trial data from ClinicalTrials.gov API v2.
    Filters by condition at API level and by phase manually in Python.
    """
    params = {
        "format": "json",
        "pageSize": max_results,
    }
    if condition:
        params["query.term"] = condition

    response = requests.get(BASE_URL, params=params)

    # --- Check for HTTP issues ---
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")

    # --- Check content ---
    if not response.text.strip():
        raise Exception("Empty response from ClinicalTrials.gov API — check parameters")

    try:
        data = response.json()
    except Exception:
        print("Response is not valid JSON. Here's a preview:\n")
        print(response.text[:500])
        raise

    trials = []
    for study in data.get("studies", []):
        proto = study.get("protocolSection", {})
        id_mod = proto.get("identificationModule", {})
        status_mod = proto.get("statusModule", {})
        design_mod = proto.get("designModule", {})
        cond_mod = proto.get("conditionsModule", {})
        loc_mod = proto.get("contactsLocationsModule", {})

        locations = loc_mod.get("locations", [])
        for loc in locations:
            facility = loc.get("facility")
            if isinstance(facility, dict):
                facility_name = facility.get("name")
            elif isinstance(facility, str):
                facility_name = facility
            else:
                facility_name = None

            trials.append({
                "nct_id": id_mod.get("nctId"),
                "title": id_mod.get("briefTitle"),
                "status": status_mod.get("overallStatus"),
                "phase": design_mod.get("phases"),
                "condition": ", ".join(cond_mod.get("conditions", [])) if cond_mod.get("conditions") else None,
                "facility": facility_name,
                "city": loc.get("city"),
                "country": loc.get("country"),
                "last_update": status_mod.get("lastUpdatePostDateStruct", {}).get("date"),
            })

    df = pd.DataFrame(trials)

    # --- Manual Phase Filter (if specified) ---
    if phase:
        df = df[df["phase"].apply(lambda x: phase in str(x))]

    print(f"✅ Fetched {len(df)} trial location records after filtering.")
    return df
