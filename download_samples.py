#!/usr/bin/env python3
"""
download_samples.py - Download and cache raw evidence samples for Workshop #1
Flood Monitoring and Risk System (Texas Scope)
"""

import os
import io
import gzip
import json
import requests
import pandas as pd

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "workshop_1", "samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)

NWS_HEADERS = {
    "User-Agent": "FloodMonitoringApp/1.0 (contact: cavirguezs@udistrital.edu.co)",
    "Accept": "application/geo+json"
}

def download_noaa_storm_events():
    print("[1/4] Fetching NOAA Storm Events 2024...")
    url = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d2024_c20260728.csv.gz"
    res = requests.get(url, stream=True, timeout=60)
    res.raise_for_status()
    
    with gzip.GzipFile(fileobj=io.BytesIO(res.content)) as gz:
        df = pd.read_csv(gz, low_memory=False)
    
    print(f"Total US records in 2024: {len(df)}")
    # Filter for Texas flood-related events
    tx_floods = df[(df['STATE'] == 'TEXAS') & (df['EVENT_TYPE'].isin(['Flood', 'Flash Flood', 'Heavy Rain']))]
    print(f"Texas flood events found: {len(tx_floods)}")
    
    sample_file = os.path.join(SAMPLES_DIR, "noaa_storm_events_texas_sample.csv")
    tx_floods.to_csv(sample_file, index=False)
    print(f"Saved: {sample_file} ({len(tx_floods)} rows)")

def download_ghcn_daily():
    print("[2/4] Fetching GHCN-Daily Historical Precipitation for Texas stations...")
    # Key Texas airport stations: Houston (USW00012918), Austin (USW00013904), DFW (USW00023044), San Antonio (USW00012921)
    stations = "USW00012918,USW00013904,USW00023044,USW00012921"
    url = f"https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations={stations}&startDate=2023-01-01&endDate=2024-06-30&dataTypes=PRCP,TMAX,TMIN&format=json"
    res = requests.get(url, timeout=30)
    res.raise_for_status()
    data = res.json()
    print(f"GHCN-Daily records fetched: {len(data)}")
    
    sample_file = os.path.join(SAMPLES_DIR, "ghcn_daily_texas_sample.json")
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {sample_file}")

def download_nws_observations():
    print("[3/4] Fetching NWS Station Observations for Texas...")
    stations = ["KHOU", "KAUS", "KDFW", "KSAT", "KCRP"]
    all_features = []
    
    for st in stations:
        url = f"https://api.weather.gov/stations/{st}/observations?limit=100"
        try:
            r = requests.get(url, headers=NWS_HEADERS, timeout=15)
            if r.status_code == 200:
                feats = r.json().get("features", [])
                print(f"Station {st}: {len(feats)} observations")
                all_features.extend(feats)
        except Exception as e:
            print(f"Failed to fetch station {st}: {e}")
            
    print(f"Total NWS observations collected: {len(all_features)}")
    sample_file = os.path.join(SAMPLES_DIR, "nws_observations_sample.json")
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": all_features}, f, indent=2)
    print(f"Saved: {sample_file}")

def download_nws_alerts():
    print("[4/4] Fetching NWS Texas Alerts (Active & Recent)...")
    url = "https://api.weather.gov/alerts?area=TX&limit=300"
    res = requests.get(url, headers=NWS_HEADERS, timeout=20)
    res.raise_for_status()
    data = res.json()
    features = data.get("features", [])
    print(f"NWS Texas alerts fetched: {len(features)}")
    
    sample_file = os.path.join(SAMPLES_DIR, "nws_alerts_sample.json")
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {sample_file}")

if __name__ == "__main__":
    download_noaa_storm_events()
    download_ghcn_daily()
    download_nws_observations()
    download_nws_alerts()
    print("\nAll 4 source samples successfully downloaded and cached in workshop_1/samples/!")
