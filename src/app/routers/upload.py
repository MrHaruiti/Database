from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import tempfile
import os

from src.import_engine.importer import process_csv

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/flights")
async def upload_flights(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload single CSV file and process flights."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        result = process_csv(tmp_path)
        os.unlink(tmp_path)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
