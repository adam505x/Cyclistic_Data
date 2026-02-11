import json
import os
import random
import time
from pathlib import Path

import grequests
import requests

# Base paths (everything stays inside scraping_tool/)
BASE_DIR = Path(__file__).resolve().parent.parent
MISSING_DIR = BASE_DIR / "MissingPersons"

# Constants (conservative / polite settings)
SEARCH_LIMIT = 10000
REQUEST_BATCH_SIZE = 25   # smaller batches for stability
REQUEST_FEEDBACK_INTERVAL = 50  # fewer logs
USER_AGENT = "NamUs Scraper / Academic Research Project"

# Endpoints
API_ENDPOINT = "https://www.namus.gov/api"
STATE_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/States"
CASE_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/{type}/Cases/{case}"
SEARCH_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/{type}/Search"

# Only Missing Persons for this project
CASE_TYPES = {
    "MissingPersons": {"stateField": "stateOfLastContact"},
}

completedCases = 0

def main():
    print("Fetching states list from NamUs...")
    states_resp = requests.get(STATE_ENDPOINT, headers={"User-Agent": USER_AGENT})
    if states_resp.status_code != 200:
        print(f"Error fetching states: {states_resp.status_code}")
        return
    
    states = states_resp.json()

    for caseType in CASE_TYPES:
        print(f"\nTargeting Case Type: {caseType}")

        # Process ALL states (set to True if you want to resume at Tennessee)
        start_skipping = False  

        for state in states:
            state_name = state["name"]
            
            # --- CHECKPOINT LOGIC ---
            if start_skipping:
                if state_name == "Tennessee":
                    start_skipping = False  # Found Tennessee, start processing now
                else:
                    print(f" > Skipping {state_name} (already processed)")
                    continue
            # -------------------------

            global completedCases
            completedCases = 0
            print(f"--- Processing State: {state_name} ---")
            
            # ... rest of your existing scraping logic continues here ...

            # Search for IDs specifically in this state to avoid the 10k national limit
            search_payload = {
                "take": SEARCH_LIMIT,
                "projections": ["namus2Number"],
                "predicates": [
                    {
                        "field": CASE_TYPES[caseType]["stateField"],
                        "operator": "IsIn",
                        "values": [state_name],
                    }
                ],
            }

            search_response = requests.post(
                SEARCH_ENDPOINT.format(type=caseType),
                headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
                data=json.dumps(search_payload)
            )

            if search_response.status_code != 200:
                print(f" > Error searching {state_name}: {search_response.status_code}")
                continue

            cases = search_response.json().get("results", [])
            total_in_state = len(cases)
            print(f" > Found {total_in_state} cases in {state_name}")

            if total_in_state == 0:
                continue

            # Output path per state (Best practice for Big Data partitioning)
            safe_state_name = state_name.replace(" ", "_")
            MISSING_DIR.mkdir(parents=True, exist_ok=True)
            file_path = MISSING_DIR / f"{safe_state_name}.json"

            print(f" > Exporting to {file_path}")
            with file_path.open("w", encoding="utf-8") as outputFile:
                outputFile.write("[")

                # Track whether we've already written at least one valid case
                first_written = True

                # Process cases in batches
                for i in range(0, total_in_state, REQUEST_BATCH_SIZE):
                    batch = cases[i : i + REQUEST_BATCH_SIZE]
                    
                    caseRequests = (
                        grequests.get(
                            CASE_ENDPOINT.format(type=caseType, case=c["namus2Number"]),
                            hooks={"response": requestFeedback},
                            headers={"User-Agent": USER_AGENT},
                        )
                        for c in batch
                    )

                    responses = grequests.map(caseRequests)
                    
                    for resp in responses:
                        if resp and resp.status_code == 200:
                            # Comma between items only (avoids trailing comma issues)
                            if not first_written:
                                outputFile.write(",")
                            outputFile.write(resp.text)
                            first_written = False
                    
                    # Politeness delay between batches to reduce errors / throttling
                    time.sleep(random.uniform(0.5, 1.5))

                outputFile.write("]")
            
            print(f" > Finished {state_name}\n")

    print("Master scrape completed successfully.")

def requestFeedback(response, **kwargs):
    global completedCases
    completedCases += 1
    if completedCases % REQUEST_FEEDBACK_INTERVAL == 0:
        print(f"   - Progress: {completedCases} case details downloaded...")


if __name__ == "__main__":
    main()