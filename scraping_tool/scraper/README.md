## NamUs scraper

Small, standalone scraper for the NamUs Missing Persons API plus a linker that turns the JSON into a CSV.

Works on Windows, macOS, and Linux.

---

### 1. Set up environments

From the **project root** (`billionaires-1`):

**Windows (PowerShell)**

```powershell
cd "C:\Users\Adam McIntyre\billionaires-1"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r scraping_tool/scraper/requirements.txt
```

**macOS / Linux (bash/zsh)**

```bash
cd /path/to/billionaires-1
python3 -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r scraping_tool/scraper/requirements.txt
```

---

### 2. Run the scraper

From the project root (or any directory), using the venv’s Python:

```bash
python scraping_tool/scraper/main.py
```

This calls the NamUs API and writes JSON to:

- `scraping_tool/MissingPersons/<STATE>.json`

---

### 3. Build the CSV

```bash
python scraping_tool/scraper/linker.py
```

This reads all JSON in `scraping_tool/MissingPersons/` and writes:

- `scraping_tool/output/NamUs_Master_Robust_v3.csv` (de‑duplicated by `NamUs_ID`).



