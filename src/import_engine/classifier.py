from __future__ import annotations
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any
from .rules import DEFAULT_RULES, FlightRules

def classify_movement(
    raw: Dict[str, Any],
    rules: FlightRules = DEFAULT_RULES
) -> Tuple[str, Dict[str, Any]]:
    """
    Classify single row as arrival, departure or both.
    
    Returns:
        classification: 'arrival', 'departure', or 'both'
        enriched_row: dict with computed missing fields
    """
    enriched = raw.copy()
    
    # Parse times - handle NaN values from pandas
    actual_time = None
    if raw.get("actual_time") and str(raw["actual_time"]) != "nan":
        actual_time = datetime.fromisoformat(raw["actual_time"])
    
    schedule_time = None
    if raw.get("schedule_time") and str(raw["schedule_time"]) != "nan":
        schedule_time = datetime.fromisoformat(raw["schedule_time"])
    
    # Determine aircraft type
    ac_type = raw.get("ac_type", "A320")
    tat = rules.get_turnaround(ac_type)
    
    # Call-sign parity rule (odd = departure, even = arrival)
    callsign = raw.get("callsign", "")
    is_odd = int(callsign[-1]) % 2 == 1 if callsign and callsign[-1].isdigit() else None
    
    # Check if both actual_in and actual_out are provided
    has_actual_in = raw.get("actual_in") and str(raw.get("actual_in")) != "nan"
    has_actual_out = raw.get("actual_out") and str(raw.get("actual_out")) != "nan"
    
    if has_actual_in and has_actual_out:
        classification = "both"
    elif actual_time:
        # Single entry - decide based on callsign parity (reversed logic: odd=departure, even=arrival)
        if is_odd is True:
            classification = "departure"
            enriched["actual_out"] = actual_time.isoformat()
            enriched["actual_in"] = (actual_time - tat).isoformat()
        else:
            classification = "arrival"
            enriched["actual_in"] = actual_time.isoformat()
            enriched["actual_out"] = (actual_time + tat).isoformat()
    elif schedule_time:
        # Use schedule time with same logic
        if is_odd is True:
            classification = "departure"
            enriched["scheduled_out"] = schedule_time.isoformat()
            enriched["scheduled_in"] = (schedule_time - tat).isoformat()
        else:
            classification = "arrival"
            enriched["scheduled_in"] = schedule_time.isoformat()
            enriched["scheduled_out"] = (schedule_time + tat).isoformat()
    else:
        classification = "unknown"
    
    return classification, enriched
