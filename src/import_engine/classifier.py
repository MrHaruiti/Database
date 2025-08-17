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
    
    REGRAS PRÉ-ESTABELECIDAS (EXATAS DO SISTEMA MANUAL):
    1. Empresas Estrangeiras: Cálculo automático da partida com TAT correto
    2. Emirates: Pop-up para inserção manual do horário de partida
    
    TAT Rules:
    - ICAO [O,H,V,L,U,G,D,E,F] + Narrowbody: 60min
    - ICAO [O,H,V,L,U,G,D,E,F] + Widebody: 120min  
    - Other ICAO + Narrowbody: 120min
    - Other ICAO + Widebody: 180min
    
    Returns:
        classification: 'arrival', 'departure', or 'both'
        enriched_row: dict with computed missing fields
    """
    enriched = raw.copy()
    
    # Parse times - handle NaN values from pandas and multiple time formats
    actual_time = None
    if raw.get("actual_time") and str(raw["actual_time"]) != "nan":
        time_str = str(raw["actual_time"]).strip()
        try:
            # Try ISO format first
            actual_time = datetime.fromisoformat(time_str)
        except ValueError:
            try:
                # Try HH:MM format (add current date)
                if ':' in time_str and len(time_str.split(':')) == 2:
                    from datetime import date
                    today = date.today()
                    actual_time = datetime.strptime(f"{today} {time_str}", "%Y-%m-%d %H:%M")
                else:
                    raise ValueError(f"Unsupported time format: {time_str}")
            except ValueError as e:
                raise ValueError(f"Cannot parse time '{time_str}': {e}")
    
    schedule_time = None
    if raw.get("schedule_time") and str(raw["schedule_time"]) != "nan":
        time_str = str(raw["schedule_time"]).strip()
        try:
            schedule_time = datetime.fromisoformat(time_str)
        except ValueError:
            try:
                if ':' in time_str and len(time_str.split(':')) == 2:
                    from datetime import date
                    today = date.today()
                    schedule_time = datetime.strptime(f"{today} {time_str}", "%Y-%m-%d %H:%M")
                else:
                    raise ValueError(f"Unsupported time format: {time_str}")
            except ValueError as e:
                raise ValueError(f"Cannot parse schedule time '{time_str}': {e}")
    
    # Get aircraft type and ICAO for TAT calculation
    ac_type = raw.get("ac_type", "A320")
    icao = raw.get("icao", "")
    
    # Calculate TAT using EXACT rules from manual system
    tat = rules.get_turnaround(ac_type, icao)
    
    # Identificar se é Emirates
    callsign = raw.get("callsign", "")
    flight_no = raw.get("flight_no", "")
    airline = raw.get("airline", "")
    is_emirates = (
        "UAE" in callsign.upper() or 
        "EMIRATES" in airline.upper() or
        "UAE" in flight_no.upper()
    )
    
    # Check if both actual_in and actual_out are provided
    has_actual_in = raw.get("actual_in") and str(raw.get("actual_in")) != "nan"
    has_actual_out = raw.get("actual_out") and str(raw.get("actual_out")) != "nan"
    
    if has_actual_in and has_actual_out:
        # Ambos os tempos fornecidos
        classification = "both"
    elif actual_time:
        classification = "arrival"
        enriched["actual_in"] = actual_time.isoformat()
        
        if is_emirates:
            # EMIRATES: Marcar para pop-up manual
            enriched["requires_manual_departure"] = True
            enriched["departure_status"] = "PENDING_MANUAL_INPUT"
            enriched["popup_message"] = f"Voo Emirates {callsign}: Insira horário de partida manualmente"
            # Não calcular partida automaticamente
        else:
            # EMPRESAS ESTRANGEIRAS: Cálculo automático com TAT CORRETO
            enriched["actual_out"] = (actual_time + tat).isoformat()
            enriched["departure_status"] = "AUTO_CALCULATED"
            enriched["tat_used"] = f"{tat.total_seconds()/60:.0f}min"
            enriched["tat_rule"] = f"ICAO:{icao[0] if icao else 'X'}, AC:{ac_type}, Type:{'NB' if rules.is_narrowbody(ac_type) else 'WB'}"
            
    elif schedule_time:
        classification = "arrival"
        enriched["scheduled_in"] = schedule_time.isoformat()
        
        if is_emirates:
            # EMIRATES: Marcar para pop-up manual
            enriched["requires_manual_departure"] = True
            enriched["departure_status"] = "PENDING_MANUAL_INPUT"
            enriched["popup_message"] = f"Voo Emirates {callsign}: Insira horário de partida manualmente"
        else:
            # EMPRESAS ESTRANGEIRAS: Cálculo automático com TAT CORRETO
            enriched["scheduled_out"] = (schedule_time + tat).isoformat()
            enriched["departure_status"] = "AUTO_CALCULATED"
            enriched["tat_used"] = f"{tat.total_seconds()/60:.0f}min"
            enriched["tat_rule"] = f"ICAO:{icao[0] if icao else 'X'}, AC:{ac_type}, Type:{'NB' if rules.is_narrowbody(ac_type) else 'WB'}"
    else:
        classification = "unknown"
    
    return classification, enriched
