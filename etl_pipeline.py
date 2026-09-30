"""
Bluestock Fintech - Mutual Fund Analytics Platform
Deliverable: etl_pipeline.py (Master Ingestion and Pipeline Orchestrator)
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_etl():
    print("=" * 70)
    print("BLUESTOCK FINTECH - MASTER ETL DATA PIPELINE")
    print("=" * 70)
    
    # 1. Run Data Ingestion and Live NAV Fetch
    print("\n[STEP 1/2] Executing Data Ingestion (data_ingestion.py)...")
    subprocess.run([sys.executable, str(BASE_DIR / "data_ingestion.py")], check=True)
    
    # 2. Run Data Cleaning and SQLite Star Schema
    print("\n[STEP 2/2] Executing Data Cleaning and SQLite Star Schema (scripts/data_cleaning.py)...")
    subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "data_cleaning.py")], check=True)
    
    print("\n" + "=" * 70)
    print("MASTER ETL PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_etl()
