import pytest
from datetime import datetime, timedelta
from src.import_engine.classifier import classify_movement
from src.import_engine.rules import FlightRules

def test_classify_arrival_only():
    """Test classification when only arrival time provided (even callsign)."""
    raw = {
        "callsign": "ABY124",  # Even number = arrival
        "ac_type": "A320",
        "actual_time": "2024-06-01T08:00:00",
        "schedule_time": "2024-06-01T08:00:00"
    }
    classification, enriched = classify_movement(raw)
    assert classification == "arrival"
    assert "actual_in" in enriched
    assert "actual_out" in enriched

def test_classify_departure_only():
    """Test classification when only departure time provided (odd callsign)."""
    raw = {
        "callsign": "ABY123",  # Odd number = departure
        "ac_type": "A320",
        "actual_time": "2024-06-01T08:00:00"
    }
    classification, enriched = classify_movement(raw)
    assert classification == "departure"
    assert "actual_out" in enriched
    assert "actual_in" in enriched

def test_classify_both_times():
    """Test classification when both times provided."""
    raw = {
        "callsign": "ABY125",
        "ac_type": "A320",
        "actual_in": "2024-06-01T08:00:00",
        "actual_out": "2024-06-01T08:45:00"
    }
    classification, enriched = classify_movement(raw)
    assert classification == "both"

def test_turnaround_calculation():
    """Test turnaround time calculation."""
    rules = FlightRules()
    assert rules.get_turnaround("A320") == timedelta(minutes=45)
    assert rules.get_turnaround("ATR72") == timedelta(minutes=25)
