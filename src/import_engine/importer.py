import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from .classifier import classify_movement
from .rules import DEFAULT_RULES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("import.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ["actual_time"]  # Only time is truly required
OPTIONAL_FIELDS = ["flight_no", "callsign", "ac_type"]  # These can be auto-generated

# Map columns from your CSV to the expected names in the code
COLUMN_MAP = {
    'FlightNumber': 'flight_no',
    'ICAO': 'icao',  # Map to icao field, not callsign
    'Aircraft': 'ac_type',
    'Time': 'actual_time',
    'Destination': 'cidade',
    'Airline': 'companhia',
    'Country': 'pais',
    'TPS': 'tps',
    'Status': 'status'
}

def process_csv(file_path: str) -> Dict[str, Any]:
    """Process single CSV file and return summary."""
    logger.info(f"Starting import from {file_path}")
    df = pd.read_csv(file_path)
    
    # Mapeamento automático dos nomes das colunas
    for csv_col, expected_col in COLUMN_MAP.items():
        if csv_col in df.columns and expected_col not in df.columns:
            df[expected_col] = df[csv_col]
            logger.info(f"Mapped column '{csv_col}' to '{expected_col}'.")

    logger.info(f"Loaded {len(df)} rows")
    
    arrivals = []
    departures = []
    warnings = []
    
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        # Fill missing required fields with sensible defaults and log warnings
        for field in REQUIRED_FIELDS:
            if field not in row_dict or pd.isna(row_dict[field]) or str(row_dict[field]).strip() == "":
                warnings.append(f"Row {idx}: Missing required field '{field}'. Skipping row.")
                continue
        
        # Fill missing optional fields with auto-generated values
        for field in OPTIONAL_FIELDS:
            if field not in row_dict or pd.isna(row_dict[field]) or str(row_dict[field]).strip() == "":
                if field == "ac_type":
                    row_dict[field] = "A320"  # Default aircraft
                elif field == "callsign":
                    # Generate callsign from airline + flight number
                    airline = str(row_dict.get("companhia", ""))
                    flight_no = str(row_dict.get("flight_no", ""))
                    if airline and flight_no:
                        # Create callsign from first letters of airline + flight number
                        airline_code = ''.join([word[0] for word in airline.split() if word])[:3].upper()
                        row_dict[field] = f"{airline_code}{flight_no}"
                    else:
                        row_dict[field] = f"AUTO_CALL_{idx}"
                elif field == "flight_no":
                    row_dict[field] = f"FLT{idx+1000}"  # Generate flight number

        try:
            classification, enriched = classify_movement(row_dict)
            if classification in ["arrival", "both"]:
                arrivals.append(enriched)
            if classification in ["departure", "both"]:
                departures.append(enriched)
            if classification == "arrival" and "actual_out" in enriched:
                dep_row = enriched.copy()
                dep_row["actual_in"] = None
                dep_row["classification"] = "departure"
                departures.append(dep_row)
        except Exception as e:
            warning = f"Row {idx}: {str(e)}"
            warnings.append(warning)
            logger.warning(warning)
    
    if departures:
        departures_df = pd.DataFrame(departures)
        departures_df = departures_df.drop_duplicates()
        departures = departures_df.to_dict(orient="records")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    if arrivals:
        pd.DataFrame(arrivals).to_csv(output_dir / "arrivals.csv", index=False)
    if departures:
        pd.DataFrame(departures).to_csv(output_dir / "departures.csv", index=False)
    
    summary = {
        "rows_received": len(df),
        "arrivals_created": len(arrivals),
        "departures_created": len(departures),
        "warnings": warnings
    }
    
    logger.info(f"Import complete: {summary}")
    return summary

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m src.import_engine.importer <file.csv>")
        sys.exit(1)
    
    result = process_csv(sys.argv[1])
    print(result)