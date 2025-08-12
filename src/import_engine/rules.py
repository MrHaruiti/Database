from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict

@dataclass
class FlightRules:
    """Centralized business rules for flight processing."""
    tat_matrix: Dict[str, timedelta] = None
    tps_domestic_gates: set[str] = None
    tps_international_gates: set[str] = None
    night_stop_hour: int = 2  # 02:00 local

    def __post_init__(self):
        if self.tat_matrix is None:
            self.tat_matrix = {
                "A320": timedelta(minutes=45),
                "B737": timedelta(minutes=45),
                "A330": timedelta(minutes=60),
                "B777": timedelta(minutes=60),
                "ATR72": timedelta(minutes=25),
                "Q400": timedelta(minutes=25),
            }
        if self.tps_domestic_gates is None:
            self.tps_domestic_gates = {"A1", "A2", "A3", "B1", "B2"}
        if self.tps_international_gates is None:
            self.tps_international_gates = {"C1", "C2", "C3", "D1", "D2"}

    def get_turnaround(self, ac_type: str) -> timedelta:
        """Return turnaround time for given aircraft type."""
        return self.tat_matrix.get(ac_type, timedelta(minutes=45))

    def is_night_stop(self, arrival: str, departure: str) -> bool:
        """Determine if aircraft remains overnight."""
        # Simplified: if arrival before 02:00 and departure after 05:00
        return True  # Placeholder for real logic

DEFAULT_RULES = FlightRules()
