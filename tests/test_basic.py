"""
Basic sanity tests for project structure and configuration.
"""

import os
import yaml

def test_config_sources_exists():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "sources.yaml")
    assert os.path.exists(config_path), "sources.yaml must exist"
    
    with open(config_path, "r", encoding="utf-8") as f:
        conf = yaml.safe_load(f)
        
    assert "sources" in conf
    sources = conf["sources"]
    assert "noaa_storm_events" in sources
    assert "ghcn_daily" in sources
    assert "nws_observations" in sources
    assert "nws_alerts" in sources

def test_samples_exist_and_non_empty():
    samples_dir = os.path.join(os.path.dirname(__file__), "..", "workshop_1", "samples")
    assert os.path.exists(samples_dir), "samples folder must exist"
    
    files = [
        "noaa_storm_events_texas_sample.csv",
        "ghcn_daily_texas_sample.json",
        "nws_observations_sample.json",
        "nws_alerts_sample.json"
    ]
    for filename in files:
        filepath = os.path.join(samples_dir, filename)
        assert os.path.exists(filepath), f"{filename} must exist"
        assert os.path.getsize(filepath) > 0, f"{filename} cannot be empty"
