import requests
import pandas as pd

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def fetch_trials(condition=None, phase=None, max_results=100):
    params = {
        "format": "json",
        "pageSize": max_results,
    }
    if condition:
        params["cond"] = condition
    if phase:
        params["phase"] = phase

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    trials = []
    for study in data.get("studies", []):
        info = study.get("protocolSection", {}).get("identificationModule", {})
        locations = study.get("protocolSection", {}).get("contactsLocationsModule", {}).get("locations", [])
        for loc in locations:
            trials.append({
                "nct_id": study.get("protocolSection", {}).get("identificationModule", {}).get("nctId"),
                "title": info.get("briefTitle"),
                "status": study.get("protocolSection", {}).get("statusModule", {}).get("overallStatus"),
                "phase": study.get("protocolSection", {}).get("designModule", {}).get("phases"),
                "condition": ", ".join(study.get("protocolSection", {}).get("conditionsModule", {}).get("conditions", [])),
                "intervention_type": ", ".join([i["type"] for i in study.get("protocolSection", {}).get("armsInterventionsModule", {}).get("interventions", [])]) if study.get("protocolSection", {}).get("armsInterventionsModule") else None,
                "facility": loc.get("facility", {}).get("name"),
                "city": loc.get("city"),
                "country": loc.get("country"),
                "last_update": study.get("protocolSection", {}).get("statusModule", {}).get("lastUpdatePostDateStruct", {}).get("date"),
            })
    return pd.DataFrame(trials)
