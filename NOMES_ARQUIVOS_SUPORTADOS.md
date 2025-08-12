# 📁 Nomes de Arquivos Suportados

## ✅ **QUALQUER NOME CSV É ACEITO!**

Você pode usar **qualquer nome** para seus arquivos CSV:

### Exemplos de Nomes Válidos:
```bash
✅ voos_janeiro_2024.csv
✅ importacao_massiva.csv
✅ chegadas_hoje.csv
✅ dados_aeroporto.csv
✅ flights_data.csv
✅ meus_voos.csv
✅ backup_voos_123.csv
✅ planilha_operacoes.csv
```

### Como Usar:
```bash
# Qualquer um destes comandos funciona:
python -m src.import_engine.importer voos_janeiro_2024.csv
python -m src.import_engine.importer importacao_massiva.csv
python -m src.import_engine.importer chegadas_hoje.csv
python -m src.import_engine.importer dados_aeroporto.csv
```

### Via API FastAPI:
```bash
POST /upload/flights
# Aceita qualquer arquivo .csv independente do nome
```

## 🚫 **Única Restrição:**
- Arquivo **DEVE ter extensão .csv**
- Conteúdo deve seguir o formato CSV padrão

## 📋 **Formato do Conteúdo (Independente do Nome):**
```csv
flight_no,callsign,ac_type,actual_time
TAM3002,TAM3002,A320,2024-06-01T08:15:00
GOL1004,GLO1004,B737,2024-06-01T10:30:00
```

## 🎯 **Resumo:**
- ✅ **Nome do arquivo**: Totalmente livre (desde que termine em .csv)
- ✅ **Localização**: Qualquer pasta
- ✅ **Tamanho**: Sem limite (otimizado para milhares de linhas)
- ✅ **Encoding**: UTF-8 recomendado
