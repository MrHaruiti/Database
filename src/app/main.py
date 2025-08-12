from fastapi import FastAPI
from src.app.routers.upload import router as upload_router

app = FastAPI(
    title="Sistema de Importação de Voos",
    description="API para importação otimizada de dados de voos com entrada única",
    version="1.0.0"
)

app.include_router(upload_router)

@app.get("/")
async def root():
    return {
        "message": "Sistema de Importação de Voos - API Ativa",
        "endpoints": {
            "upload": "/upload/flights (POST - CSV file)",
            "docs": "/docs"
        }
    }
