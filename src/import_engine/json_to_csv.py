import json
import pandas as pd
from datetime import datetime
from pathlib import Path

def convert_json_to_csv(json_file: str, output_csv: str = None) -> str:
    """Convert JSON flight data to CSV format compatible with import system."""
    
    # Read JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        flights = json.load(f)
    
    # Convert to CSV format
    csv_data = []
    for flight in flights:
        # Map aircraft types to standard ICAO codes
        ac_type_mapping = {
            'A306': 'A300',
            'B735': 'B737',
            'MD83': 'MD83',
            'B734': 'B737',
            'A320': 'A320',
            'B733': 'B737',
            'A321': 'A321',
            'B77W': 'B777',
            'A333': 'A330',
            'A359': 'A350',
            'B78X': 'B787',
            'B789': 'B787',
            'B788': 'B787',
            'A388': 'A380'
        }
        
        # Create callsign from airline and flight
        airline_codes = {
            'MERAJ AIRLINES': 'MRJ',
            'VARESH AIRLINES': 'VRH',
            'QESHM AIR': 'QSM',
            'ZAGROS AIRLINES': 'ZAG',
            'PARS AIR': 'PRS',
            'ATA AIRLINES': 'ATA',
            'KARUN AIRLINES': 'KRN',
            'IRAN AIR': 'IRA',
            'AIR CHINA': 'CCA',
            'HAINAN AIRLINES': 'CHH',
            'SICHUAN AIRLINES': 'CSC',
            'AMERICAN AIRLINES': 'AAL',
            'DELTA AIRLINES': 'DAL',
            'UNITED AIRLINES': 'UAL',
            'VIRGIN ATLANTIC USA': 'VIR',
            'EMIRATES AIRLINES': 'UAE'
        }
        
        airline_code = airline_codes.get(flight['AIRLINE'], 'UNK')
        callsign = f"{airline_code}{flight['FLIGHT']}"
        
        # Convert time to full datetime (assuming today's date)
        time_str = flight['TIME']
        actual_time = f"2024-06-01T{time_str}:00"
        
        # Determine domestic/international based on country
        dom_intl = 'dom' if flight['COUNTRY'] == 'IRAN' else 'intl'
        
        # Map aircraft type
        ac_type = ac_type_mapping.get(flight['A/C'], flight['A/C'])
        
        csv_row = {
            'flight_no': f"{airline_code}{flight['FLIGHT']}",
            'callsign': callsign,
            'ac_type': ac_type,
            'reg': f"EP-{flight['FLIGHT']}",  # Dummy registration
            'actual_time': actual_time,
            'destination': flight['DESTINATION'],
            'icao': flight['ICAO'],
            'country': flight['COUNTRY'],
            'terminal': f"T{flight['TPS'] // 3 + 1}",  # Map TPS to terminal
            'gate': f"A{flight['TPS']}",
            'dom_intl': dom_intl,
            'tps': flight['TPS'],
            'status': flight['STATUS']
        }
        
        csv_data.append(csv_row)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(csv_data)
    
    if output_csv is None:
        output_csv = json_file.replace('.json', '_converted.csv')
    
    df.to_csv(output_csv, index=False)
    print(f"✅ Converted {len(flights)} flights from {json_file} to {output_csv}")
    
    return output_csv

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m src.import_engine.json_to_csv <file.json>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    csv_file = convert_json_to_csv(json_file)
    print(f"CSV file created: {csv_file}")
