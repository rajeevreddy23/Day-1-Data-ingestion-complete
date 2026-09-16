"""
Bluestock Fintech - Mutual Fund Analytics Platform
Master Execution Pipeline: run_pipeline.py

Orchestrates the complete capstone analytics lifecycle:
1. Environment & Directory Setup
2. Day 1: Data Ingestion & Live NAV Fetch (mfapi.in)
3. Day 2: Data Cleaning, Normalization & SQLite Star-Schema Database Population
4. Day 4: Quantitative Fund Performance Analytics & Benchmark Chart Generation
5. Day 6: Advanced Risk Analytics (VaR, CVaR, HHI, Recommender Engine)
6. Final Deliverable Verification & Dashboard Readiness Check
"""

import os
import sys
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def log_section(title: str):
    print("\n" + "=" * 80)
    print(f" {title.upper()}")
    print("=" * 80)

def run_step(step_name: str, script_path: Path):
    print(f"\n[RUNNING] {step_name} ({script_path.name})...")
    start_time = time.time()
    result = subprocess.run([sys.executable, str(script_path)], capture_output=False)
    elapsed = time.time() - start_time
    if result.returncode == 0:
        print(f"[SUCCESS] {step_name} completed in {elapsed:.2f} seconds.")
    else:
        print(f"[ERROR] {step_name} failed with exit code {result.returncode}!")
        sys.exit(result.returncode)

def verify_deliverables():
    log_section("Verifying Final Project Deliverables")
    expected_files = [
        ("Final_Report.pdf", "Executive Final Project Report (15-20 pages)"),
        ("Bluestock_MF_Presentation.pptx", "Executive 12-Slide Presentation Deck"),
        ("README.md", "Complete Project Documentation"),
        ("requirements.txt", "Pinned Dependencies"),
        ("data/processed/clean_nav.csv", "Cleaned Historical NAV Dataset"),
        ("data/processed/fund_scorecard.csv", "Composite Fund Scorecard (0-100)"),
        ("data/processed/alpha_beta.csv", "Alpha & Beta Regression vs Nifty 100"),
        ("data/processed/var_cvar_report.csv", "VaR & CVaR Risk Analysis Report"),
        ("benchmark_comparison_chart.png", "Top 5 Funds vs Benchmark Growth Chart"),
        ("rolling_sharpe_chart.png", "90-Day Rolling Sharpe Ratio Chart"),
        ("scripts/compute_metrics.py", "Quantitative Metrics Calculation Engine"),
        ("scripts/recommender.py", "Algorithmic Fund Recommender Engine"),
        ("dashboard/capstone_dashboard.py", "Interactive Streamlit Web Dashboard")
    ]
    
    all_present = True
    for rel_path, desc in expected_files:
        p = BASE_DIR / rel_path
        if p.exists():
            print(f"  [OK] {rel_path:<35} - {desc}")
        else:
            print(f"  [MISSING] {rel_path:<35} - {desc}")
            all_present = False
            
    if all_present:
        print("\nAll deliverables verified present and complete!")
    else:
        print("\nWarning: Some deliverable files are missing.")

def main():
    start_total = time.time()
    log_section("Bluestock Fintech - Master Capstone Analytics Pipeline")
    print(f"Working Directory: {BASE_DIR}")
    print(f"Python Runtime   : {sys.version.split()[0]}")

    # Step 1: Ingestion
    run_step("Step 1: Data Ingestion & Live NAV API", BASE_DIR / "data_ingestion.py")

    # Step 2: Data Cleaning & SQL Star Schema
    run_step("Step 2: Data Cleaning & SQLite Database", BASE_DIR / "scripts" / "data_cleaning.py")

    # Step 3: Performance Metrics & Scorecards
    run_step("Step 3: Fund Performance Metrics", BASE_DIR / "scripts" / "compute_metrics.py")

    # Step 4: Advanced Analytics & Risk Metrics
    run_step("Step 4: Advanced Analytics & Risk", BASE_DIR / "notebooks" / "06_advanced_analytics.py")

    # Step 5: Deliverable Verification
    verify_deliverables()

    total_time = time.time() - start_total
    log_section("Capstone Pipeline Execution Completed Successfully")
    print(f"Total Execution Time: {total_time:.2f} seconds")
    print("\nTo launch the interactive analytical web dashboard:")
    print("  streamlit run dashboard/capstone_dashboard.py\n")

if __name__ == "__main__":
    main()
