"""
pipeline/step0_download.py
--------------------------
STEP 0: Download and extract Cyclistic/Divvy trip data from AWS S3.

WHY THIS STEP EXISTS (rubric requirement):
  The professor must be able to clone the repo and run the project without
  manually downloading or moving any files. This script handles the entire
  data acquisition automatically.

WHAT IT DOES:
  - Downloads monthly .zip files for 2020-2022 from the public AWS S3 bucket:
    https://divvy-tripdata.s3.amazonaws.com/
  - Extracts each zip to data/raw/
  - Skips files already downloaded (safe to re-run)
  - Records download time via StepTimer

NOTE ON SCHEMA CHANGE:
  Divvy changed their CSV column names in April 2020. The Q1 2020 file uses
  the old schema. Step 1 normalises both schemas before concatenating.

  Old schema (2020-Q1):  trip_id, start_time, end_time, from_station_name, ...
  New schema (2020-04+): ride_id, started_at, ended_at, start_station_name, ...
"""

import os
import sys
import zipfile
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.metrics import StepTimer

# ── Configuration ─────────────────────────────────────────────────────────────

RAW_DIR  = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
BASE_URL = "https://divvy-tripdata.s3.amazonaws.com/"

# Q1 2020 has a unique filename and the old column schema
Q1_2020 = ["Divvy_Trips_2020_Q1.zip"]

# Apr-Dec 2020 (standard naming, new schema)
FILES_2020 = [f"2020{m:02d}-divvy-tripdata.zip" for m in range(4, 13)]

# All of 2021 and 2022
FILES_2021_2022 = [
    f"{year}{m:02d}-divvy-tripdata.zip"
    for year in [2021, 2022]
    for m in range(1, 13)
]

ALL_FILES = Q1_2020 + FILES_2020 + FILES_2021_2022


# ── Helpers ────────────────────────────────────────────────────────────────────

def download_file(filename: str, dest_dir: str) -> str:
    local_path = os.path.join(dest_dir, filename)
    if os.path.exists(local_path):
        print(f"  [skip] {filename} already downloaded.")
        return local_path
    url = BASE_URL + filename
    print(f"  [download] {filename} ...", end=" ", flush=True)
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    size_mb = os.path.getsize(local_path) / (1024 * 1024)
    print(f"done ({size_mb:.1f} MB)")
    return local_path


def extract_zip(zip_path: str, dest_dir: str):
    with zipfile.ZipFile(zip_path, "r") as z:
        for member in z.namelist():
            if not member.endswith(".csv"):
                continue
            # Skip macOS resource fork files (._filename.csv)
            if os.path.basename(member).startswith('._'):
                continue
            out_path = os.path.join(dest_dir, os.path.basename(member))
            if os.path.exists(out_path):
                print(f"  [skip] {os.path.basename(member)} already extracted.")
                continue
            print(f"  [extract] {os.path.basename(member)}")
            with z.open(member) as src, open(out_path, "wb") as dst:
                dst.write(src.read())

    # Delete the zip file after successful extraction to save disk space
    os.remove(zip_path)
    print(f"  [deleted] {os.path.basename(zip_path)}")


# ── Main entry point ───────────────────────────────────────────────────────────

def run():
    os.makedirs(RAW_DIR, exist_ok=True)
    files = ALL_FILES
    print(f"\n=== STEP 0: Download & Extract | {len(files)} files ===")

    with StepTimer("step0_download"):
        for filename in files:
            try:
                zip_path = download_file(filename, RAW_DIR)
                extract_zip(zip_path, RAW_DIR)
            except requests.HTTPError as e:
                print(f"  [WARNING] Could not download {filename}: {e}")

    print(f"\n  Raw CSVs are in: {os.path.abspath(RAW_DIR)}")


if __name__ == "__main__":
    run()
