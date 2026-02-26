"""
run.py
-------
Data preparation entry point for the Cyclistic Big Data project.
Cross-platform: works on Linux, macOS, and Windows.

RESPONSIBILITY:
  This script covers the data acquisition and cleaning layer (Steps 0 & 1).
  The output — data/processed/trips_clean.csv — is consumed by the analysis
  notebooks maintained by other team members.

USAGE:
    # From the project root:
    python -m pipeline.run                        # Full run (2020-2022)
    python -m pipeline.run --prototype            # 2020 only (Section 2 baseline)
    python -m pipeline.run --skip-download        # Skip download, re-run clean only
    python -m pipeline.run --steps 0              # Run a single step
    python -m pipeline.run --help

STEPS:
    0 - Download & extract raw data from AWS S3
    1 - Load, normalise schema, clean, output trips_clean.csv
"""

import sys
import os
import argparse
import time

if __package__ is None or __package__ == "":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from pipeline import step0_download, step1_linker
else:
    from . import step0_download, step1_linker

STEPS = {
    0: ("Download & Extract", step0_download),
    1: ("Load & Clean",       step1_linker),
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cyclistic Data Preparation Pipeline (Steps 0 & 1)"
    )
    parser.add_argument(
        "--prototype",
        action="store_true",
        help="Download 2020 data only (~4M rows). Use for Section 2 baseline.",
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

    mode_label = "PROTOTYPE (2020 only)" if args.prototype else "FULL (2020-2022)"

    print("\n" + "=" * 60)
    print("  CYCLISTIC — DATA PREPARATION PIPELINE")
    print("  COMP30770 Programming for Big Data")
    print(f"  Mode: {mode_label}")
    print("=" * 60)
    print(f"  Steps to run: {steps_to_run}\n")

    overall_start = time.perf_counter()

    for step_num in steps_to_run:
        name, module = STEPS[step_num]
        print(f"{'─' * 60}")
        try:
            if step_num == 0:
                module.run(prototype=args.prototype)
            else:
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
