"""
pipeline/step1_load_clean.py
-----------------------------
STEP 1: Load all raw CSVs, normalise column names, and combine into one file.

WHAT THIS STEP DOES:
  - Loads all CSV files from data/raw/
  - Normalises the schema difference between the old (2020-Q1) and new column
    names so all files can be concatenated cleanly
  - Saves the combined file to data/processed/trips_clean.csv
  - Deletes the individual raw CSVs after the combined file is saved

NOTE — NO CLEANING IS PERFORMED HERE:
  Row-level cleaning (null handling, filtering, deduplication) is intentionally
  left to the analysis notebooks. This step only ensures a consistent schema
  across all files.

SCHEMA CHANGE:
  Divvy changed column names in April 2020.

  Old schema (2020-Q1):  trip_id, start_time, end_time, from_station_name, ...
  New schema (2020-04+): ride_id, started_at, ended_at, start_station_name, ...

  We rename old columns to match the new schema before concatenating.

INPUTS:  data/raw/*.csv
OUTPUTS: data/processed/trips_clean.csv
"""

import os
import sys
import glob
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.metrics import StepTimer

# ── Paths ──────────────────────────────────────────────────────────────────────

RAW_DIR       = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUTPUT_FILE   = os.path.join(PROCESSED_DIR, "trips_clean.csv")

# ── Column mapping for OLD schema (2020 Q1) ────────────────────────────────────

OLD_TO_NEW_COLUMNS = {
    "trip_id":           "ride_id",
    "start_time":        "started_at",
    "end_time":          "ended_at",
    "from_station_name": "start_station_name",
    "from_station_id":   "start_station_id",
    "to_station_name":   "end_station_name",
    "to_station_id":     "end_station_id",
    "usertype":          "member_casual",
}

# Columns we keep in the final output (drops old-schema-only fields like
# bikeid, tripduration, gender, birthyear which have no new-schema equivalent)
REQUIRED_COLUMNS = [
    "ride_id",
    "rideable_type",
    "started_at",
    "ended_at",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id",
    "start_lat",
    "start_lng",
    "end_lat",
    "end_lng",
    "member_casual",
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def load_and_normalise_csv(filepath: str) -> pd.DataFrame:
    """
    Load a single CSV and normalise it to the standard schema.
    Handles both old (2020-Q1) and new column formats.
    """
    df = pd.read_csv(filepath, low_memory=False)

    # Detect old schema by looking for a key old-schema column
    if "from_station_name" in df.columns:
        df = df.rename(columns=OLD_TO_NEW_COLUMNS)

        # Old schema stores user type as "Subscriber"/"Customer"
        # Standardise to "member"/"casual" to match the new schema
        df["member_casual"] = df["member_casual"].str.lower().replace(
            {"subscriber": "member", "customer": "casual"}
        )

    # Keep only the columns common to both schemas
    available = [c for c in REQUIRED_COLUMNS if c in df.columns]
    return df[available]


# ── Main entry point ───────────────────────────────────────────────────────────

def run():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print("\n=== STEP 1: Load & Combine ===")

    csv_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DIR}. Did Step 0 run successfully?"
        )

    print(f"  Found {len(csv_files)} CSV files.")

    with StepTimer("step1_load_combine"):
        frames = []
        for i, filepath in enumerate(csv_files, 1):
            fname = os.path.basename(filepath)
            print(f"  [{i}/{len(csv_files)}] Loading {fname} ...", end=" ", flush=True)
            df = load_and_normalise_csv(filepath)
            print(f"{len(df):,} rows")
            frames.append(df)

        print("  Concatenating all files ...")
        combined = pd.concat(frames, ignore_index=True)

        print(f"  Total rows: {combined.shape[0]:,}")
        print(f"  Columns: {list(combined.columns)}")

        combined.to_csv(OUTPUT_FILE, index=False)
        print(f"  Saved to: {os.path.abspath(OUTPUT_FILE)}")

        # Delete individual raw CSVs now that the combined file is saved
        print("  Removing raw CSV files ...")
        for filepath in csv_files:
            os.remove(filepath)
            print(f"  [deleted] {os.path.basename(filepath)}")

        print(f"  Done. {len(csv_files)} raw CSVs removed.")


if __name__ == "__main__":
    run()
