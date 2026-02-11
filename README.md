# NAMUS Missing Persons Analysis
COMP30770 - Programming for Big Data

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Install Dependencies

**Windows:**
```powershell
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

**Mac/Linux:**
```bash
.venv/bin/python -m pip install -r requirements.txt
```

### 4. Configure CSV Path

Create a `.env` file in the project root directory with your local CSV file path:

```env
NAMUS_CSV_PATH=C:\Users\YourName\NAMUS_Missing_Persons\scraping_tool\output\NamUs_Master_Robust_v3.csv
```

**Note:** If your path contains spaces, you can use quotes (optional but recommended):
```env
NAMUS_CSV_PATH="C:\Users\Your Name\NAMUS_Missing_Persons\scraping_tool\output\NamUs_Master_Robust_v3.csv"
```

**Important:** The `.env` file is not committed to git (it's in `.gitignore`). Each team member needs to create their own.

## Project Structure

- `main.ipynb` - Main analysis notebook
- `scraping_tool/` - Scraping tool and output directory
- `requirements.txt` - Python dependencies
- `.env` - Your local CSV path configuration (create this yourself)
