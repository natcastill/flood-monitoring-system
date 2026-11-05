-- Initial Schema Definitions for Flood Monitoring System (Texas Scope)
-- Workshop #1 - Common Data Model and Flood Domain Tables
-- Team 2: Oscar Durán, Laura Pardo, Nicolás Romero

-- 1. Source Catalog Table
CREATE TABLE IF NOT EXISTS source (
    source_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    format VARCHAR(64) NOT NULL,
    license VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Ingestion Audit Runs Table
CREATE TABLE IF NOT EXISTS ingestion_run (
    run_id VARCHAR(64) PRIMARY KEY,
    source_id VARCHAR(64) REFERENCES source(source_id),
    mode VARCHAR(32) NOT NULL, -- 'historical', 'incremental'
    started TIMESTAMPTZ NOT NULL,
    finished TIMESTAMPTZ,
    status VARCHAR(32) NOT NULL, -- 'RUNNING', 'SUCCESS', 'FAILED'
    rows_in INTEGER DEFAULT 0,
    rows_new INTEGER DEFAULT 0,
    rows_rejected INTEGER DEFAULT 0
);

-- 3. Ingestion State (High-Water Mark per Source)
CREATE TABLE IF NOT EXISTS ingestion_state (
    source_id VARCHAR(64) PRIMARY KEY REFERENCES source(source_id),
    watermark VARCHAR(255) NOT NULL,
    last_success TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 4. Canonical Event Table
CREATE TABLE IF NOT EXISTS event (
    event_id VARCHAR(128) PRIMARY KEY,
    source_id VARCHAR(64) REFERENCES source(source_id),
    event_type VARCHAR(64) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    severity VARCHAR(32) NOT NULL,
    raw_reference TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_event_timestamp ON event(timestamp);
CREATE INDEX IF NOT EXISTS idx_event_coords ON event(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_event_type ON event(event_type);

-- 5. Event Group Table (Cross-source matching)
CREATE TABLE IF NOT EXISTS event_group (
    group_id VARCHAR(128) NOT NULL,
    event_id VARCHAR(128) NOT NULL REFERENCES event(event_id),
    group_type VARCHAR(64) DEFAULT 'PHYSICAL_EVENT_CLUSTER',
    confidence_score NUMERIC(5, 4),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, event_id)
);

-- 6. Rejected Records (Quarantine)
CREATE TABLE IF NOT EXISTS rejected_record (
    quarantine_id VARCHAR(64) PRIMARY KEY,
    run_id VARCHAR(64) REFERENCES ingestion_run(run_id),
    source_id VARCHAR(64) REFERENCES source(source_id),
    reason TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 7. Domain Table: Flood Event Details
CREATE TABLE IF NOT EXISTS flood_event_details (
    event_id VARCHAR(128) PRIMARY KEY REFERENCES event(event_id) ON DELETE CASCADE,
    flood_cause VARCHAR(128),
    county_name VARCHAR(128),
    county_fips VARCHAR(10),
    property_damage_usd NUMERIC(15, 2) DEFAULT 0.00,
    direct_deaths INTEGER DEFAULT 0,
    direct_injuries INTEGER DEFAULT 0,
    narrative TEXT
);

-- 8. Domain Table: Precipitation Reading Details
CREATE TABLE IF NOT EXISTS precipitation_reading_details (
    event_id VARCHAR(128) PRIMARY KEY REFERENCES event(event_id) ON DELETE CASCADE,
    station_id VARCHAR(64) NOT NULL,
    station_name VARCHAR(255),
    precip_amount_mm NUMERIC(8, 2) NOT NULL,
    accumulation_interval_hours INTEGER DEFAULT 24,
    temp_max_c NUMERIC(5, 2),
    temp_min_c NUMERIC(5, 2),
    quality_flag VARCHAR(32) DEFAULT 'PASSED'
);
