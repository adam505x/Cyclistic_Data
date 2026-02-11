import csv
import glob
import json
import os
from pathlib import Path

import pandas as pd

# Base paths (everything stays inside scraping_tool/)
BASE_DIR = Path(__file__).resolve().parent.parent
MISSING_DIR = BASE_DIR / "MissingPersons"
OUTPUT_DIR = BASE_DIR / "output"

# CONFIGURATION
INPUT_PATH = str(MISSING_DIR / "*.json")
OUTPUT_FILE = OUTPUT_DIR / "NamUs_Master_Robust_v3.csv"

def get_path(data, paths):
    """
    The 'Pathfinder' function.
    Args:
        data: The JSON dictionary for a case.
        paths: A list of strings representing keys (e.g., "subjectDescription.hairColor.name")
    Returns:
        The first valid value found, or None.
    """
    for path in paths:
        current = data
        try:
            # Navigate down the dot-notation path
            for key in path.split('.'):
                if isinstance(current, dict):
                    current = current.get(key)
                elif isinstance(current, list) and key.isdigit():
                    current = current[int(key)]
                else:
                    current = None
                    break
            
            # If we found something not None/Empty
            if current is not None and str(current).strip() not in ['', 'None', 'nan', '[]']:
                return str(current).strip()
        except:
            continue
    return None

def extract_lists(data, list_key, name_keys, separator=" | "):
    """Safely extracts lists of objects (like clothing or features)."""
    items = data.get(list_key, [])
    if not items or not isinstance(items, list):
        return ""
    
    results = []
    for item in items:
        # Try to find the name using the provided keys
        val = get_path(item, name_keys)
        desc = item.get("description")
        
        full = val if val else ""
        if desc:
            full = f"{full}: {desc}" if full else desc
        if full:
            results.append(full)
            
    return separator.join(results)

def main():
    json_files = glob.glob(INPUT_PATH)
    print(f"--- UNIVERSAL ROBUST EXTRACTION ---")
    print(f"Found {len(json_files)} state files.")
    
    all_cases = []
    
    for file_path in json_files:
        # Safety: Skip non-JSON or the output file itself
        if not file_path.endswith('.json') or "NamUs" in file_path:
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                state_data = json.load(f)
                if not isinstance(state_data, list): continue
                
                for case in state_data:
                    # ==========================================
                    # 1. IDENTITY & STATUS
                    # ==========================================
                    namus_id = get_path(case, ["idFormatted", "namus2Number", "id"])
                    status = get_path(case, ["publicationStatus.name", "publicationStatus"])
                    date_mod = case.get("modifiedDateTime")
                    
                    # NCMEC Logic
                    ncmec = "No"
                    if case.get("hasNcmecContributors") or case.get("hasPendingByNcmec"):
                        ncmec = "Yes"

                    # ==========================================
                    # 2. PERSONAL DETAILS
                    # ==========================================
                    first = get_path(case, ["subjectIdentification.firstName", "firstname"])
                    last = get_path(case, ["subjectIdentification.lastName", "lastname"])
                    middle = get_path(case, ["subjectIdentification.middleName", "middlename"])
                    nicknames = get_path(case, ["subjectIdentification.nicknames", "nicknames"])
                    
                    # Age: Prioritize manual entry over computed
                    age_current = get_path(case, ["subjectIdentification.currentMaxAge", "subjectIdentification.computedCurrentMaxAge", "computedCurrentMaxAge"])
                    age_missing = get_path(case, ["subjectIdentification.missingMaxAge", "subjectIdentification.computedMissingMaxAge", "computedMissingMaxAge"])
                    
                    sex = get_path(case, ["subjectDescription.sex.name", "gender.name", "gender"])
                    
                    # Race: Loop through ethnicities list
                    race_list = case.get("subjectDescription", {}).get("ethnicities", [])
                    if not race_list: race_list = case.get("raceEthnicity", []) # Fallback
                    if isinstance(race_list, list):
                        races = [get_path(r, ["name"]) for r in race_list if get_path(r, ["name"])]
                        race_final = ", ".join(races)
                    else:
                        race_final = str(race_list)

                    # Tribal
                    tribe_list = case.get("subjectDescription", {}).get("tribeAssociations", [])
                    tribes = [get_path(t, ["tribe.name"]) for t in tribe_list if get_path(t, ["tribe.name"])]
                    tribe_final = ", ".join(tribes)

                    # ==========================================
                    # 3. PHYSICAL DESCRIPTION
                    # ==========================================
                    # Hair & Eyes (Handle dictionary vs string)
                    hair = get_path(case, ["physicalDescription.hairColor.name", "subjectDescription.hairColor.name", "physicalDescription.hairColor"])
                    
                    # Eyes: Check Left, Right, then Generic
                    eyes = get_path(case, ["physicalDescription.leftEyeColor.name", "physicalDescription.eyeColor.name", "physicalDescription.eyeColor"])

                    # Height Range
                    h_min = get_path(case, ["subjectDescription.heightFrom", "physicalDescription.heightFrom"])
                    h_max = get_path(case, ["subjectDescription.heightTo", "physicalDescription.heightTo"])
                    height = f"{h_min}" if h_min == h_max else f"{h_min} - {h_max}"

                    # Weight Range
                    w_min = get_path(case, ["subjectDescription.weightFrom", "physicalDescription.weightFrom"])
                    w_max = get_path(case, ["subjectDescription.weightTo", "physicalDescription.weightTo"])
                    weight = f"{w_min}" if w_min == w_max else f"{w_min} - {w_max}"

                    # ==========================================
                    # 4. LOCATION & DATE
                    # ==========================================
                    city = get_path(case, ["sighting.address.city", "cityOfLastContact"])
                    state = get_path(case, ["sighting.address.state.name", "stateOfLastContact.name", "stateOfLastContact"])
                    county = get_path(case, ["sighting.address.county.name", "countyOfLastContact"])
                    zip_code = get_path(case, ["sighting.address.zipCode"])
                    date_last_seen = get_path(case, ["sighting.date", "dateOfLastContact"])

                    # ==========================================
                    # 5. AGENCIES (The "Maze" Logic)
                    # ==========================================
                    agencies = case.get("investigatingAgencies", [])
                    ag_results = []
                    for ag in agencies:
                        # Path A (Deep - PA/AL) vs Path B (Shallow - TX)
                        name = get_path(ag, ["selection.agency.name", "name"])
                        type_ = get_path(ag, ["selection.agency.agencyType.name", "agencyType.name"])
                        case_num = ag.get("caseNumber")
                        date_rep = ag.get("dateReported")
                        
                        # Contact Info
                        c_first = get_path(ag, ["selection.contact.firstName"])
                        c_last = get_path(ag, ["selection.contact.lastName"])
                        c_phone = get_path(ag, ["selection.contact.phone", "selection.agency.phone"])
                        c_email = get_path(ag, ["selection.contact.email", "selection.agency.email"])
                        
                        # Build Agency String
                        entry_parts = [name]
                        if type_: entry_parts.append(f"({type_})")
                        if case_num: entry_parts.append(f"[Case#: {case_num}]")
                        if date_rep: entry_parts.append(f"[Rep: {date_rep}]")
                        
                        contact_parts = []
                        if c_first: contact_parts.append(f"Det. {c_first} {c_last or ''}")
                        if c_phone: contact_parts.append(f"Ph: {c_phone}")
                        if c_email: contact_parts.append(f"Email: {c_email}")
                        
                        if contact_parts:
                            entry_parts.append(f"-- {' '.join(contact_parts)}")
                            
                        ag_results.append(" ".join(entry_parts))
                    
                    agency_final = " | ".join(ag_results)

                    # ==========================================
                    # 6. VEHICLES, CLOTHING, CIRCUMSTANCES
                    # ==========================================
                    # Vehicles
                    vehicles = case.get("vehicles", [])
                    veh_results = []
                    for v in vehicles:
                        year = get_path(v, ["vehicleYear", "year"])
                        make = get_path(v, ["vehicleMake.name", "make"])
                        model = get_path(v, ["vehicleModel.name", "model"])
                        color = get_path(v, ["vehicleColor.name", "color"])
                        tag = get_path(v, ["tagNumber", "licencePlateNumber"])
                        
                        desc = f"{year or ''} {make or ''} {model or ''}".strip()
                        if color: desc += f" [{color}]"
                        if tag: desc += f" (Tag: {tag})"
                        if desc: veh_results.append(desc)
                    vehicle_final = " | ".join(veh_results)

                    # Clothing
                    # Checks both "clothingAndAccessoriesArticles" (New) and "clothingAndAccessories" (Old)
                    clothing_final = extract_lists(case, "clothingAndAccessoriesArticles", ["category.name", "article.name"])
                    if not clothing_final:
                        clothing_final = extract_lists(case, "clothingAndAccessories", ["category.name"])

                    # Distinctive Features
                    # Checks both "physicalFeatureDescriptions" (New) and "physicalIdentifiers" (Old)
                    features_final = extract_lists(case, "physicalFeatureDescriptions", ["physicalFeature.name"])
                    if not features_final:
                        features_final = extract_lists(case, "physicalIdentifiers", ["type.name"])

                    # Circumstances
                    circ = get_path(case, ["circumstances.circumstancesOfDisappearance", "circumstances"])
                    if circ: circ = circ.replace('\n', ' ').replace('\r', ' ')

                    # ==========================================
                    # 7. FORENSICS & IMAGES
                    # ==========================================
                    dna = get_path(case, ["dnaStatus.status"]) or "Unknown"
                    dental = get_path(case, ["dentalStatus.status"]) or "Unknown"
                    fingerprint = get_path(case, ["fingerprintStatus.status"]) or "Unknown"
                    
                    images = case.get("images", [])
                    captions = [img.get("caption") for img in images if img.get("caption")]
                    caption_str = " | ".join(captions)

                    # BUILD ROW
                    clean_case = {
                        "NamUs_ID": namus_id,
                        "Status": status,
                        "Modified_Date": date_mod,
                        "First_Name": first,
                        "Last_Name": last,
                        "Nicknames": nicknames,
                        "Missing_Age": age_missing,
                        "Current_Age": age_current,
                        "Sex": sex,
                        "Race": race_final,
                        "Tribal_Affiliation": tribe_final,
                        "Height": height,
                        "Weight": weight,
                        "Hair": hair,
                        "Eyes": eyes,
                        "City": city,
                        "County": county,
                        "State": state,
                        "Zip": zip_code,
                        "Date_Last_Seen": date_last_seen,
                        "Agencies": agency_final,
                        "Vehicles": vehicle_final,
                        "Clothing": clothing_final,
                        "Physical_Features": features_final,
                        "Circumstances": circ,
                        "NCMEC": ncmec,
                        "DNA": dna,
                        "Dental": dental,
                        "Fingerprints": fingerprint,
                        "Has_Images": "Yes" if images else "No",
                        "Image_Captions": caption_str
                    }
                    all_cases.append(clean_case)
                    
            except Exception as e:
                # print(f"Skipping bad record in {os.path.basename(file_path)}: {e}")
                pass

    # SAVE
    if all_cases:
        df = pd.DataFrame(all_cases)
        df.drop_duplicates(subset=['NamUs_ID'], inplace=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUTPUT_FILE, index=False, quoting=csv.QUOTE_ALL)
        print(f"SUCCESS! Processed {len(all_cases)} records into {len(df)} unique cases.")
        print(f"Saved to: {OUTPUT_FILE}")
    else:
        print("No cases found.")

if __name__ == "__main__":
    main()