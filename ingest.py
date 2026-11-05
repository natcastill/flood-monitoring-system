#!/usr/bin/env python3
"""
ingest.py - Unified Command-Line Entry Point
Flood Monitoring and Risk System (Texas Scope)
Data Analysis Programming - Semester 2026-II
Team 2: Oscar Durán, Laura Pardo, Nicolás Romero
"""

import argparse
import sys
import logging
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ingest-cli")

def run_historical(start_date: str = None, end_date: str = None):
    """
    Historical bulk ingestion mode.
    Populates historical baseline (2019-2024) idempotently.
    """
    logger.info(f"Starting historical bulk ingestion. Start: {start_date}, End: {end_date}")
    # Workshop 1: Stub implementation
    print("\n==========================================")
    print(" MODE: HISTORICAL BULK INGESTION (STUB)   ")
    print("==========================================")
    print(f"Target Period : {start_date or '2019-01-01'} -> {end_date or '2024-12-31'}")
    print("Sources       : NOAA Storm Events (CSV.GZ), GHCN-Daily (JSON)")
    print("Status        : Ready for Workshop #2 pipeline execution.\n")

def run_incremental():
    """
    Incremental ingestion mode.
    Retrieves observations and active alerts using watermarks.
    """
    logger.info("Starting incremental ingestion run.")
    # Workshop 1: Stub implementation
    print("\n==========================================")
    print(" MODE: INCREMENTAL INGESTION (STUB)       ")
    print("==========================================")
    print("Sources       : NWS Station Observations, NWS Active Alerts")
    print("Watermark     : last_success -> NOW")
    print("Status        : Ready for Workshop #3 pipeline execution.\n")

def run_status():
    """
    Audit status mode.
    Displays watermarks, last runs, and row counts.
    """
    logger.info("Retrieving system ingestion status.")
    print("\n==========================================")
    print(" SYSTEM INGESTION AUDIT STATUS (STUB)     ")
    print("==========================================")
    print(f"Current Time  : {datetime.now(timezone.utc).isoformat()}")
    print("Source Status :")
    print("  - noaa_storm_events : Configured (Watermark: BEGIN_DATE_TIME)")
    print("  - ghcn_daily        : Configured (Watermark: DATE)")
    print("  - nws_observations  : Configured (Watermark: timestamp)")
    print("  - nws_alerts        : Configured (Watermark: sent)")
    print("Status        : System initialized and configured.\n")

def main():
    parser = argparse.ArgumentParser(
        description="Flood Monitoring Data Ingestion Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--mode",
        choices=["historical", "incremental", "status"],
        required=True,
        help="Execution mode: 'historical' (bulk load), 'incremental' (watermark polling), or 'status' (health check)"
    )
    parser.add_argument(
        "--start",
        type=str,
        default="2019-01-01",
        help="Start date for historical mode (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end",
        type=str,
        default="2024-12-31",
        help="End date for historical mode (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    if args.mode == "historical":
        run_historical(start_date=args.start, end_date=args.end)
    elif args.mode == "incremental":
        run_incremental()
    elif args.mode == "status":
        run_status()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
