# Cyclistic Data Analysis Project
COMP30770 - Programming for Big Data


### 1. Clone the Repository
```bash
git clone https://github.com/adam505x/Cyclistic_Data.git
cd Cyclistic_Data
```

### 2. Create Virtual Environment

**Mac/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Pipeline
```bash
python pipeline/run.py
```


The `create_and_join_weather.ipynb` notebook adds and links our additional data. Cells 1 + 2 create our `weather_data_clean.csv` and `weather_data.json` which is already included. 
- **RUN** cells 3+4 in `create_and_join_weather.ipynb` to link the data (This process could take 10+ minutes).

### 5. Analyses
The analysis notebooks are pre-run and saved with outputs for submission. They compare traditional methods (Pandas/SQL) on prototype data versus big data methods (Spark) on the full dataset. Our prototype, `trips_prototype_with_weather.csv`,  was created by keeping a random 1% of our final data.

- **Prototype Analyses**:
  - `pandas_prototype.ipynb`
  - `SQL_prototype.ipynb`
- **Full Dataset Analyses**:
  - `spark_analysis.ipynb` - Spark analysis on full dataset

## Project Structure

- `data/raw/` - Raw data files (used when creating final dataset)
- `data/processed/` - Processed data and analysis notebooks
  - `trips_clean.csv` - Cleaned trip data
- `pipeline/` - Data processing pipeline
  - `run.py` - Main pipeline script (runs steps 0-1)
  - `step0_download.py` - Download and extract raw trip data from AWS S3
  - `step1_linker.py` - Link and normalize all trip CSVs into combined file
  - `create_and_join_weather.ipynb` - Process weather data and join with trip data
  - `metrics.py` - Metrics calculation and timing utilities
  - `weather_data_clean.csv` - Cleaned weather data
  - `weather_data.json` - Weather data (2nd dataset)
- `Analysis/` - Analysis notebooks comparing traditional vs big data approaches
  - `pandas_prototype.ipynb` - Pandas analysis on prototype data 
  - `SQL_prototype.ipynb` - SQL analysis on prototype data 
  - `spark_analysis.ipynb` - Spark analysis on full dataset (big data method)
  - `trips_prototype_with_weather.csv` - Sample dataset (1% of full data) for prototype analyses
- `results/` - Output results
  - `metrics.json` - Calculated metrics
- `requirements.txt` - Python dependencies

