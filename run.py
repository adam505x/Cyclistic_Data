"""
run.py
-------
Data preparation entry point for the Cyclistic Big Data project.
Cross-platform: works on Linux, macOS, and Windows.

RESPONSIBILITY:
  This script covers the data acquisition and linking layer (Steps 0 & 1).
  The output — data/processed/trips_clean.csv — is consumed by the analysis
  notebooks maintained by other team members.

USAGE:
    python run.py                   # Run full pipeline (2020-2022)
    python run.py --skip-download   # Skip download, re-run linker only
    python run.py --steps 0         # Run a single step
    python run.py --help

STEPS:
    0 - Download & extract raw data from AWS S3
    1 - Link all CSVs into one combined file
"""

import sys
import os
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import step0_download, step1_linker

STEPS = {
    0: ("Download & Extract", step0_download),
    1: ("Link CSVs",          step1_linker),
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cyclistic Data Preparation Pipeline (Steps 0 & 1)"
    )
    parser.add_argument(
        "--steps",
        nargs="+",
        type=int,
        choices=STEPS.keys(),
        help="Run specific steps only (e.g. --steps 0 1)",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip Step 0 (use if raw data is already downloaded)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    steps_to_run = sorted(args.steps) if args.steps else list(STEPS.keys())
    if args.skip_download and 0 in steps_to_run:
        steps_to_run.remove(0)

    print("\n" + "=" * 60)
    print("  CYCLISTIC — DATA PREPARATION PIPELINE")
    print("  COMP30770 Programming for Big Data")
    print("=" * 60)
    print(f"  Steps to run: {steps_to_run}\n")

    overall_start = time.perf_counter()

    for step_num in steps_to_run:
        name, module = STEPS[step_num]
        print(f"{'─' * 60}")
        try:
            module.run()
        except Exception as e:
            print(f"\n  ✗ Step {step_num} ({name}) FAILED: {e}")
            sys.exit(1)

    elapsed = time.perf_counter() - overall_start
    print(f"\n{'=' * 60}")
    print(f"  Done. Total time: {elapsed:.1f}s")
    print(f"  Output: data/processed/trips_clean.csv")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()