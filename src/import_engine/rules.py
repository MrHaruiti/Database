from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Set

@dataclass
class FlightRules:
    """Centralized business rules for flight processing - REGRAS EXATAS DO SISTEMA MANUAL."""
    
    # ICAO groups for TAT calculation
    icao_group_special: Set[str] = None
    
    # Narrowbody aircraft types (from manual system)
    narrowbody_types: Set[str] = None
    
    # TPS gate assignments
    tps_domestic_gates: Set[str] = None
    tps_international_gates: Set[str] = None
    night_stop_hour: int = 2  # 02:00 local

    def __post_init__(self):
        if self.icao_group_special is None:
            # ICAO codes that get special TAT treatment
            self.icao_group_special = {'O', 'H', 'V', 'L', 'U', 'G', 'D', 'E', 'F'}
        
        if self.narrowbody_types is None:
            # EXACT narrowbody list from manual system
            self.narrowbody_types = {
                'B722', 'B731', 'B732', 'B733', 'B734', 'B735', 'B736', 'B737', 
                'B738', 'B739', 'B73X', 'A318', 'A319', 'A320', 'A321', 'E170', 
                'E175', 'E190', 'E195', 'MD81', 'MD82', 'MD83', 'MD86', 'MD87', 
                'MD88', 'MD89', 'MD90', 'AT72', 'AT75', 'AT76', 'AT42', 'AT43', 
                'AT45', 'AT46', 'E110', 'E120', 'E135', 'E140', 'E145', 'L410'
            }
            
        if self.tps_domestic_gates is None:
            self.tps_domestic_gates = {"A1", "A2", "A3", "B1", "B2"}
        if self.tps_international_gates is None:
            self.tps_international_gates = {"C1", "C2", "C3", "D1", "D2"}

    def is_narrowbody(self, ac_type: str) -> bool:
        """Check if aircraft is narrowbody based on EXACT manual system rules."""
        if not ac_type:
            return True  # Default to narrowbody
        return ac_type.upper() in self.narrowbody_types

    def is_widebody(self, ac_type: str) -> bool:
        """Check if aircraft is widebody."""
        return not self.is_narrowbody(ac_type)

    def is_special_icao_group(self, icao: str) -> bool:
        """Check if ICAO belongs to special group (O, H, V, L, U, G, D, E, F)."""
        if not icao or len(icao) < 1:
            return False
        return icao[0].upper() in self.icao_group_special

    def get_turnaround(self, ac_type: str, icao: str) -> timedelta:
        """
        Calculate TAT based on EXACT rules from manual system:
        
        ICAO Group [O,H,V,L,U,G,D,E,F]:
        - Narrowbody: 60 min
        - Widebody: 120 min
        
        Other ICAO:
        - Narrowbody: 120 min  
        - Widebody: 180 min
        """
        is_special_icao = self.is_special_icao_group(icao)
        is_narrow = self.is_narrowbody(ac_type)
        
        if is_special_icao:
            if is_narrow:
                return timedelta(minutes=60)   # 1h
            else:
                return timedelta(minutes=120)  # 2h
        else:
            if is_narrow:
                return timedelta(minutes=120)  # 2h
            else:
                return timedelta(minutes=180)  # 3h

    def is_night_stop(self, arrival: str, departure: str) -> bool:
        """Determine if aircraft remains overnight."""
        # Simplified: if arrival before 02:00 and departure after 05:00
        return True  # Placeholder for real logic

DEFAULT_RULES = FlightRules()
