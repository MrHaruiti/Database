import csv
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

def process_csv(file_path: str) -> Dict[str, Any]:
    """Process single CSV file and return summary."""
    logger.info(f"Starting import from {file_path}")
    
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {len(df)} rows")
    
    arrivals = []
    departures = []
    warnings = []
    
    for idx, row in df.iterrows():
        try:
            classification, enriched = classify_movement(row.to_dict())
            
            if classification in ["arrival", "both"]:
                arrivals.append(enriched)
            if classification in ["departure", "both"]:
                departures.append(enriched)
                
        except Exception as e:
            warning = f"Row {idx}: {str(e)}"
            warnings.append(warning)
            logger.warning(warning)
    
    # Save results
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
