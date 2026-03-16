"""
create_prototype.py
--------------------
ONE-TIME SCRIPT — run by the data preparation team member only.

Creates a representative prototype dataset by randomly sampling 5-10% of
rows from the full trips_clean.csv. The output is committed to the repo
and used by the analysis notebooks for Section 2 baseline testing.

This script is NOT intended to be run by the professor. It is documented
here for transparency and covered in the project writeup.

INPUTS:  data/processed/trips_clean.csv
OUTPUTS: prototype/trips_prototype.csv

USAGE:
    python create_prototype.py
"""

import os
import sys
import pandas as pd

# ── Configuration ──────────────────────────────────────────────────────────────

INPUT_FILE  = os.path.join("data", "processed", "trips_clean.csv")
OUTPUT_DIR  = "prototype"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "trips_prototype.csv")

# Keep 7% of rows — large enough to be representative, small enough to commit
SAMPLE_FRACTION = 0.01 

# For reproducibility — using the same seed always produces the same sample
RANDOM_SEED = 42


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        print("Run the full pipeline first: python run.py")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Loading {INPUT_FILE} ...")
    df = pd.read_csv(INPUT_FILE, low_memory=False)
    full_rows = len(df)
    print(f"  Full dataset: {full_rows:,} rows")

    print(f"Sampling {SAMPLE_FRACTION * 100:.0f}% of rows ...")
    prototype = df.sample(frac=SAMPLE_FRACTION, random_state=RANDOM_SEED)
    prototype = prototype.reset_index(drop=True)
    proto_rows = len(prototype)
    print(f"  Prototype dataset: {proto_rows:,} rows ({proto_rows/full_rows*100:.1f}% of full)")

    prototype.to_csv(OUTPUT_FILE, index=False)
    print(f"  Saved to: {os.path.abspath(OUTPUT_FILE)}")
    print(f"\nDone. Commit prototype/trips_prototype.csv to the repo.")


if __name__ == "__main__":
    main()
