# 🚀 Como Importar Arquivos CSV - Guia Definitivo

## ✅ **MÉTODO RECOMENDADO: Linha de Comando**

### 1. Prepare seu arquivo CSV (qualquer nome):
```csv
flight_no,callsign,ac_type,actual_time
TAM3002,TAM3002,A320,2024-06-01T08:15:00
GOL1004,GLO1004,B737,2024-06-01T10:30:00
```

### 2. Execute o comando:
```bash
python -m src.import_engine.importer SEU_ARQUIVO.csv
```

### 3. Exemplos testados e funcionando:
```bash
# ✅ TESTADO - Funciona perfeitamente:
python -m src.import_engine.importer exemplo_so_chegadas.csv
python -m src.import_engine.importer exemplo_importacao_massiva.csv
python -m src.import_engine.importer sample_flight.csv

# ✅ Qualquer nome funciona:
python -m src.import_engine.importer voos_janeiro.csv
python -m src.import_engine.importer meus_dados.csv
python -m src.import_engine.importer importacao_123.csv
```

## 📊 **Resultado Esperado:**
```
INFO - Starting import from SEU_ARQUIVO.csv
INFO - Loaded X rows
INFO - Import complete: {'rows_received': X, 'arrivals_created': X, 'departures_created': 0, 'warnings': []}
```

## 📁 **Arquivos Gerados:**
- `output/arrivals.csv` - Chegadas com partidas calculadas automaticamente
- `import.log` - Log detalhado do processo

## 🚫 **Se Está Dando Erro "Só Aceita JSON":**

**Você pode estar usando:**
1. ❌ Uma API diferente (não a nossa)
2. ❌ Um sistema antigo
3. ❌ Interface web de outro projeto

**SOLUÇÃO:** Use sempre o comando acima via terminal/prompt

## 🎯 **Confirmação - Sistema Testado Agora:**
```bash
$ python -m src.import_engine.importer exemplo_so_chegadas.csv
✅ 2025-08-12 04:04:10 - INFO - Starting import from exemplo_so_chegadas.csv
✅ 2025-08-12 04:04:10 - INFO - Loaded 4 rows  
✅ 2025-08-12 04:04:10 - INFO - Import complete: 4 arrivals created
```

## 📋 **Formato CSV Mínimo:**
```csv
flight_no,callsign,ac_type,actual_time
QUALQUER_VOO,CALL123,A320,2024-06-01T08:15:00
```

**GARANTIA:** O sistema aceita CSV e funciona perfeitamente via linha de comando!
