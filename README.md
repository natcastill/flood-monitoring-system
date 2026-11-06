# Flood Monitoring and Risk System (Texas Scope)

**Course:** Data Analysis Programming (Semester 2026-II)  
**Professor:** Eng. Carlos Andrés Sierra, M.Sc.  
**Institution:** Universidad Distrital Francisco José de Caldas  
**Team 2:**
- Oscar Durán (20212020080)
- Laura Pardo (20221020146)
- Nicolás Romero (20222020023)

---

## 1. Project Overview & Hazard Definition
This system is an end-to-end data ingestion, processing, and analytical monitoring platform designed to evaluate and monitor **Flood Risk** across the state of **Texas, United States**.

Flooding is one of the most destructive natural hazards in Texas, ranging from intense flash floods in the Texas Hill Country (*Flash Flood Alley*) to slow-onset riverine and hurricane-induced coastal surges along the Gulf Coast. The goal of this system is to combine historical flood events, continuous precipitation records, and real-time station observations and alerts to compute an analytical **Flood Risk Index (LOW / MEDIUM / HIGH)** and display situational awareness via an interactive dashboard.

### Geographic and Temporal Scope
- **Geographic Scope:** State of Texas (FIPS: 48), with focus on key flood-prone river basins and urban corridors (Houston/Harris County, Austin/Travis County, Dallas-Fort Worth, San Antonio).
- **Historical Temporal Window:** 2019 – 2024 (multi-year baseline, 5+ years).
- **Near-Real-Time Window:** Rolling past 24 hours, last 7 days, and active warning feeds.

---

## 2. Data Sources
The system integrates four distinct sources covering historical archives and incremental feeds:

| Source ID | Name | Type | Format / Protocol | Update Frequency | Authentication |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `noaa_storm_events` | NOAA Storm Events Database | Historical | Yearly GZipped CSV | Monthly / Revised | None (Public Domain) |
| `ghcn_daily` | NOAA NCEI GHCN-Daily | Historical | REST JSON / CSV | Daily / On-Demand | None (Public Domain) |
| `nws_observations` | NWS Station Observations | Incremental | GeoJSON REST API | Hourly / Sub-hourly | Descriptive User-Agent |
| `nws_alerts` | NWS Active Weather Alerts | Incremental | GeoJSON / CAP REST | Continuous / Event-driven | Descriptive User-Agent |

---

## 3. Repository Structure
```text
flood-monitoring-system/
├── .env.example              # Template for environment variables and secrets
├── .gitignore                # Git ignore configuration
├── README.md                 # System overview, team info, and execution guide
├── ingest.py                 # Command-line interface entry point (stub)
├── config/
│   └── sources.yaml          # Data source metadata and ingestion policies
├── data/
│   └── raw/                  # Raw landing zone (reproducible provenance)
├── notebooks/
│   └── 01_source_profiling.ipynb # Source profiling, quality evaluation, and overlap analysis
├── workshop_1/
│   ├── mapping.md            # Canonical schema and domain mapping contracts
│   └── samples/              # Unmodified raw response samples as evidence
├── sql/                      # DDL schema definitions (canonical & domain tables)
├── dashboard/                # Plotly Dash web monitoring application
├── docs/                     # Architectural diagrams and technical specifications
├── src/                      # Ingestion, validation, and transformation modules
└── tests/
    └── fixtures/             # Recorded mock responses for automated unit tests
```

---

## 4. Execution Interface (CLI Contract)
The ingestion CLI follows the unified project specification:

```bash
# Historical ingestion
python ingest.py --mode historical --start 2019-01-01 --end 2024-12-31

# Incremental ingestion (watermark-based)
python ingest.py --mode incremental

# Audit status (watermarks, row counts, and health)
python ingest.py --mode status
```
