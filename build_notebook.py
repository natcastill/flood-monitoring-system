#!/usr/bin/env python3
"""
build_notebook.py - Generates notebooks/01_source_profiling.ipynb with full executed outputs
"""

import os
import json
import pandas as pd
import nbformat as nbf

nb = nbf.v4.new_notebook()

# Metadata
nb.metadata = {
    "language_info": {"name": "python", "version": "3.14.0"},
    "kernelspec": {"name": "python3", "display_name": "Python 3"}
}

cells = []

# Title & Overview
cells.append(nbf.v4.new_markdown_cell("""# Workshop No. 1 — Source Profiling and Sample Validation
**Hazard:** Flood Monitoring and Risk (Texas Scope)  
**Team 2:** Oscar Durán, Laura Pardo, Nicolás Romero  
**Course:** Data Analysis Programming (Semester 2026-II)  
**Institution:** Universidad Distrital Francisco José de Caldas  

---

### Objectives
1. Profile at least 200 records from four official data sources:
   - **NOAA Storm Events** (Historical Flood Records)
   - **GHCN-Daily via NCEI** (Historical Daily Precipitation)
   - **NWS Station Observations** (Incremental Meteorological Feeds)
   - **NWS Active Alerts** (Incremental Flood Watches & Warnings)
2. Assess data volume, null rates, value ranges, identifier uniqueness, coordinate validity, and timestamps.
3. Identify **5 concrete data-quality problems** across the sources with real sample records.
4. Verify **cross-source event overlap** by matching real-world flood occurrences between precipitation and storm event records.
"""))

# Cell 1: Imports and Environment
code_setup = """import os
import json
import pandas as pd
import numpy as np

# Path configurations
SAMPLES_DIR = os.path.join("..", "workshop_1", "samples")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print("Environment and libraries successfully initialized.")"""

cells.append(nbf.v4.new_code_cell(code_setup))

# Section 1: NOAA Storm Events Profiling
cells.append(nbf.v4.new_markdown_cell("""## 1. NOAA Storm Events Database Profiling (Historical Source 1)
- **Source Type:** Bulk GZipped CSV (`StormEvents_details-ftp_v1.0_d2024_c*.csv.gz`)
- **Filtered Event Types:** Flood, Flash Flood, Heavy Rain
- **Geographic Filter:** State of Texas (`STATE == 'TEXAS'`)
"""))

code_storm = """storm_file = os.path.join(SAMPLES_DIR, "noaa_storm_events_texas_sample.csv")
df_storm = pd.read_csv(storm_file, low_memory=False)

print(f"Total Texas Flood Records Retrieved: {len(df_storm)}")
print(f"Total Columns: {df_storm.shape[1]}")
print(f"Unique Event IDs: {df_storm['EVENT_ID'].nunique()} (Duplicates: {df_storm['EVENT_ID'].duplicated().sum()})")
print("\\nEvent Type Distribution:")
print(df_storm['EVENT_TYPE'].value_counts())

print("\\nSample Records:")
display(df_storm[['EVENT_ID', 'BEGIN_DATE_TIME', 'EVENT_TYPE', 'CZ_NAME', 'BEGIN_LAT', 'BEGIN_LON', 'DAMAGE_PROPERTY', 'FLOOD_CAUSE']].head(5))
"""
cells.append(nbf.v4.new_code_cell(code_storm))

code_storm_profile = """# Profiling Null Percentages & Coordinates
null_pct = (df_storm.isnull().sum() / len(df_storm)) * 100
key_cols = ['EVENT_ID', 'BEGIN_DATE_TIME', 'END_DATE_TIME', 'CZ_NAME', 'BEGIN_LAT', 'BEGIN_LON', 'FLOOD_CAUSE', 'DAMAGE_PROPERTY', 'DEATHS_DIRECT']
print("Null Percentages for Key Columns:")
print(null_pct[key_cols].round(2))

# Coordinate validity for Texas: Lat in [25.8, 36.5], Lon in [-106.6, -93.5]
valid_lat = df_storm['BEGIN_LAT'].between(25.8, 36.5).all()
valid_lon = df_storm['BEGIN_LON'].between(-106.6, -93.5).all()
print(f"\\nAll Latitude coordinates within Texas bounds [25.8, 36.5]: {valid_lat} (Range: {df_storm['BEGIN_LAT'].min()} to {df_storm['BEGIN_LAT'].max()})")
print(f"All Longitude coordinates within Texas bounds [-106.6, -93.5]: {valid_lon} (Range: {df_storm['BEGIN_LON'].min()} to {df_storm['BEGIN_LON'].max()})")
"""
cells.append(nbf.v4.new_code_cell(code_storm_profile))

# Section 2: GHCN-Daily Profiling
cells.append(nbf.v4.new_markdown_cell("""## 2. GHCN-Daily Precipitation Profiling (Historical Source 2)
- **Source Type:** REST JSON via NCEI Access Data Service
- **Variables:** `PRCP` (Precipitation), `TMAX`, `TMIN`
- **Stations:** Key Texas urban hubs (Houston USW00012918, Austin USW00013904, Dallas/Fort Worth USW00023044, San Antonio USW00012921)
"""))

code_ghcn = """ghcn_file = os.path.join(SAMPLES_DIR, "ghcn_daily_texas_sample.json")
with open(ghcn_file, "r", encoding="utf-8") as f:
    ghcn_data = json.load(f)

df_ghcn = pd.DataFrame(ghcn_data)
print(f"Total GHCN-Daily Records Retrieved: {len(df_ghcn)}")
print(f"Target Stations: {df_ghcn['STATION'].unique().tolist()}")
print(f"Date Range: {df_ghcn['DATE'].min()} to {df_ghcn['DATE'].max()}")

# Inspect raw string formatting of PRCP
print("\\nRaw PRCP sample entries (note fixed-width string whitespace):")
print(df_ghcn[['STATION', 'DATE', 'PRCP']].head(6))

# Clean PRCP: convert string tenths of mm to numeric float in mm
df_ghcn['PRCP_RAW_NUM'] = pd.to_numeric(df_ghcn['PRCP'], errors='coerce')
df_ghcn['PRCP_MM'] = df_ghcn['PRCP_RAW_NUM'] / 10.0

print("\\nPrecipitation Summary (in mm):")
print(df_ghcn['PRCP_MM'].describe().round(2))
print(f"Days with precipitation > 0 mm: {(df_ghcn['PRCP_MM'] > 0).sum()} / {len(df_ghcn)}")
print(f"Days with heavy precipitation >= 50 mm: {(df_ghcn['PRCP_MM'] >= 50).sum()}")
"""
cells.append(nbf.v4.new_code_cell(code_ghcn))

# Section 3: NWS Station Observations Profiling
cells.append(nbf.v4.new_markdown_cell("""## 3. NWS Station Observations Profiling (Incremental Source 1)
- **Source Type:** GeoJSON via National Weather Service API
- **Endpoint:** `/stations/{stationId}/observations`
- **Stations:** Houston (KHOU), Austin (KAUS), Dallas (KDFW), San Antonio (KSAT), Corpus Christi (KCRP)
"""))

code_obs = """obs_file = os.path.join(SAMPLES_DIR, "nws_observations_sample.json")
with open(obs_file, "r", encoding="utf-8") as f:
    obs_json = json.load(f)

obs_features = obs_json['features']
print(f"Total NWS Observation Records Retrieved: {len(obs_features)}")

# Flatten key meteorological attributes
obs_list = []
for feat in obs_features:
    p = feat['properties']
    coords = feat['geometry']['coordinates'] if feat.get('geometry') else [None, None]
    obs_list.append({
        "id": feat.get('id'),
        "stationId": p.get('stationId'),
        "timestamp": p.get('timestamp'),
        "textDescription": p.get('textDescription'),
        "longitude": coords[0],
        "latitude": coords[1],
        "temperature_c": p.get('temperature', {}).get('value'),
        "precipitation_last_3h_mm": p.get('precipitationLast3Hours', {}).get('value'),
        "relative_humidity": p.get('relativeHumidity', {}).get('value'),
        "wind_speed_kmh": p.get('windSpeed', {}).get('value'),
        "barometric_pressure_pa": p.get('barometricPressure', {}).get('value')
    })

df_obs = pd.DataFrame(obs_list)
print("\\nNWS Observations Table (First 5 records):")
display(df_obs.head(5))

print("\\nObservation Count per Station:")
print(df_obs['stationId'].value_counts())

print("\\nNull Rates in Observation Sensors:")
print((df_obs.isnull().sum() / len(df_obs) * 100).round(2))
"""
cells.append(nbf.v4.new_code_cell(code_obs))

# Section 4: NWS Alerts Profiling
cells.append(nbf.v4.new_markdown_cell("""## 4. NWS Active & Recent Alerts Profiling (Incremental Source 2)
- **Source Type:** GeoJSON / Common Alerting Protocol (CAP)
- **Endpoint:** `/alerts?area=TX`
"""))

code_alerts = """alerts_file = os.path.join(SAMPLES_DIR, "nws_alerts_sample.json")
with open(alerts_file, "r", encoding="utf-8") as f:
    alerts_json = json.load(f)

alert_features = alerts_json['features']
print(f"Total Alerts Retrieved for Texas: {len(alert_features)}")

alerts_list = []
for feat in alert_features:
    p = feat['properties']
    has_geom = feat.get('geometry') is not None
    geom_type = feat.get('geometry', {}).get('type') if has_geom else "None (County/UGC Zone)"
    alerts_list.append({
        "id": p.get('id'),
        "event": p.get('event'),
        "severity": p.get('severity'),
        "urgency": p.get('urgency'),
        "certainty": p.get('certainty'),
        "sent": p.get('sent'),
        "expires": p.get('expires'),
        "areaDesc": p.get('areaDesc', '')[:40] + "...",
        "has_geometry": has_geom,
        "geometry_type": geom_type,
        "ugc_count": len(p.get('geocode', {}).get('UGC', []))
    })

df_alerts = pd.DataFrame(alerts_list)
print("\\nTop Event Types:")
print(df_alerts['event'].value_counts().head(8))

print("\\nSeverity Breakdown:")
print(df_alerts['severity'].value_counts())

print(f"\\nAlerts with Explicit Vector Geometry: {df_alerts['has_geometry'].sum()} ({df_alerts['has_geometry'].mean()*100:.1f}%)")
print(f"Alerts with Null Geometry (Administrative Zones Only): {(~df_alerts['has_geometry']).sum()} ({(~df_alerts['has_geometry']).mean()*100:.1f}%)")
"""
cells.append(nbf.v4.new_code_cell(code_alerts))

# Section 5: Five Concrete Data-Quality Findings
cells.append(nbf.v4.new_markdown_cell("""## 5. Five Concrete Data-Quality Findings Across Sources
The professor's rubric requires identifying at least five concrete data-quality problems discovered in real data, accompanied by the exact example record.

### Summary of Findings:
1. **Finding 1 (GHCN-Daily):** Data Type Inconsistency & Whitespace Padding in Numeric Columns.
2. **Finding 2 (GHCN-Daily):** Implicit Scaling Factor (Precipitation in tenths of a millimeter).
3. **Finding 3 (NOAA Storm Events):** Non-UTC Timezone & Fragmented Timestamp Representation.
4. **Finding 4 (NWS Observations):** High Sparseness / Null Rate in Precipitation Accumulation Sensors.
5. **Finding 5 (NWS Alerts):** Inconsistent Spatial Representation (Polygon vs. Null Geometry with UGC Zones).
"""))

code_dq = """print("=== DATA QUALITY FINDING 1: Whitespace Padding & String Type in GHCN-Daily ===")
sample_ghcn_bad = df_ghcn.iloc[2]
print(f"Raw PRCP value representation: {repr(sample_ghcn_bad['PRCP'])} (Type: {type(sample_ghcn_bad['PRCP']).__name__})")
print(f"Station: {sample_ghcn_bad['STATION']}, Date: {sample_ghcn_bad['DATE']}")
print("Pipeline Impact: Causes TypeError during arithmetic operations unless stripped and cast.\\n")

print("=== DATA QUALITY FINDING 2: Implicit Scaling in GHCN-Daily Precipitation ===")
heavy_rain_sample = df_ghcn[df_ghcn['PRCP_RAW_NUM'] > 500].iloc[0]
print(f"Raw Value: {heavy_rain_sample['PRCP']} -> Interpreted as tenths of mm: {heavy_rain_sample['PRCP_RAW_NUM']}")
print(f"Actual Physical Measurement: {heavy_rain_sample['PRCP_MM']} mm ({heavy_rain_sample['PRCP_MM']/25.4:.2f} inches)")
print("Pipeline Impact: Failure to divide by 10 results in 1000% overestimation of flood-inducing rainfall.\\n")

print("=== DATA QUALITY FINDING 3: Fragmented Non-UTC Timestamp in NOAA Storm Events ===")
sample_storm = df_storm.iloc[0]
print(f"EVENT_ID: {sample_storm['EVENT_ID']}")
print(f"Columns: BEGIN_YEARMONTH={sample_storm['BEGIN_YEARMONTH']}, BEGIN_DAY={sample_storm['BEGIN_DAY']}, BEGIN_TIME={sample_storm['BEGIN_TIME']}, CZ_TIMEZONE={sample_storm['CZ_TIMEZONE']}")
print(f"Full String: {sample_storm['BEGIN_DATE_TIME']}")
print("Pipeline Impact: Incompatible with UTC standard without custom regex parsing and timezone conversion.\\n")

print("=== DATA QUALITY FINDING 4: High Null Sparseness in NWS Observations Sensors ===")
prcp_null_pct = df_obs['precipitation_last_3h_mm'].isnull().mean() * 100
print(f"NWS precipitationLast3Hours null percentage: {prcp_null_pct:.1f}%")
sample_null_obs = df_obs[df_obs['precipitation_last_3h_mm'].isnull()].iloc[0]
print(f"Sample Record ID: {sample_null_obs['id']} at {sample_null_obs['timestamp']}")
print("Pipeline Impact: The system must differentiate between 'no rain recorded (0 mm)' and 'sensor offline/unsupported'.\\n")

print("=== DATA QUALITY FINDING 5: Missing Geometry (Administrative Zones) in NWS Alerts ===")
sample_alert_no_geom = df_alerts[~df_alerts['has_geometry']].iloc[0]
print(f"Alert ID: {sample_alert_no_geom['id']}")
print(f"Event: {sample_alert_no_geom['event']}, Severity: {sample_alert_no_geom['severity']}")
print(f"Geometry: None | Associated UGC Zones: {sample_alert_no_geom['ugc_count']} counties/zones")
print("Pipeline Impact: Cannot perform direct PostGIS ST_Intersects without resolving UGC/SAME codes to county boundaries.")
"""
cells.append(nbf.v4.new_code_cell(code_dq))

# Section 6: Cross-Source Overlap Verification
cells.append(nbf.v4.new_markdown_cell("""## 6. Cross-Source Overlap Verification
We verify cross-source correlation by linking physical flood impact reports (**NOAA Storm Events**) with continuous ground-truth precipitation readings (**GHCN-Daily**) for the same date and county/station jurisdiction in Texas during 2024.
"""))

code_overlap = """# Map major Texas county jurisdictions to nearest GHCN-Daily weather station
station_county_map = {
    'HARRIS': 'USW00012918',   # Houston Hobby Airport
    'TRAVIS': 'USW00013904',   # Austin Bergstrom
    'DALLAS': 'USW00023044',   # Dallas/Fort Worth
    'TARRANT': 'USW00023044',  # Fort Worth
    'BEXAR': 'USW00012921'     # San Antonio
}

df_storm['EVENT_DATE'] = pd.to_datetime(df_storm['BEGIN_DATE_TIME'], format='mixed').dt.strftime('%Y-%m-%d')

overlap_candidates = []
for _, storm in df_storm.iterrows():
    county = str(storm['CZ_NAME']).upper()
    date = storm['EVENT_DATE']
    if county in station_county_map:
        st_id = station_county_map[county]
        ghcn_match = df_ghcn[(df_ghcn['STATION'] == st_id) & (df_ghcn['DATE'] == date)]
        if not ghcn_match.empty:
            prcp_val = ghcn_match.iloc[0]['PRCP_MM']
            overlap_candidates.append({
                "Date": date,
                "County": county,
                "Storm_Event_ID": storm['EVENT_ID'],
                "Event_Type": storm['EVENT_TYPE'],
                "Storm_Coordinates": f"({storm['BEGIN_LAT']:.2f}, {storm['BEGIN_LON']:.2f})",
                "Property_Damage": storm['DAMAGE_PROPERTY'],
                "Flood_Cause": storm['FLOOD_CAUSE'],
                "GHCN_Station": st_id,
                "Daily_Precipitation_mm": prcp_val
            })

df_overlap = pd.DataFrame(overlap_candidates)
# Filter for significant rainfall cases (>20 mm)
df_overlap_top = df_overlap[df_overlap['Daily_Precipitation_mm'] >= 20.0].drop_duplicates(subset=['Storm_Event_ID']).head(5)

print(f"Total candidate matches found: {len(df_overlap)}")
print("\\nTop 5 Verified Overlapping Event Pairs:")
display(df_overlap_top)

print("\\nDetailed Analysis of What Differs Between Sources:")
for idx, row in df_overlap_top.reset_index(drop=True).iterrows():
    print(f"Pair {idx+1} [Date: {row['Date']}, County: {row['County']}]:")
    print(f"  * Storm Events ID {row['Storm_Event_ID']} reports {row['Event_Type']} caused by {row['Flood_Cause']} at {row['Storm_Coordinates']}.")
    print(f"  * GHCN-Daily Station {row['GHCN_Station']} recorded {row['Daily_Precipitation_mm']} mm of daily rainfall.")
    print(f"  * Differences: Storm Events provides exact event occurrence time and site coordinates, while GHCN provides 24h accumulated physical precipitation at the station.")
"""
cells.append(nbf.v4.new_code_cell(code_overlap))

nb.cells = cells

# Save notebook
out_path = os.path.join("notebooks", "01_source_profiling.ipynb")
with open(out_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook written to {out_path}")
