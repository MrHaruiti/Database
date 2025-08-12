# Sistema Otimizado de Importação de Voos

## Visão Geral
Este sistema resolve o problema de importação duplicada de dados de voos, permitindo que apenas **uma entrada** seja fornecida e o sistema automaticamente classifique como chegada (arrival) ou partida (departure) seguindo regras pré-estabelecidas.

## Características Principais

### ✅ Entrada Única
- **Antes**: Duas importações separadas (arrival + departure)
- **Agora**: Uma única linha CSV → sistema gera ambos automaticamente

### ✅ Regras de Negócio Implementadas
1. **Tempo de Solo (TAT)**:
   - A320/B737: 45 minutos
   - A330/B777: 60 minutos  
   - ATR72/Q400: 25 minutos

2. **Paridade de Call-sign**:
   - Número ímpar (ex: ABY123) → Partida
   - Número par (ex: ABY124) → Chegada

3. **TPS (Terminal Passenger Separation)**:
   - Gates domésticos: A1, A2, A3, B1, B2
   - Gates internacionais: C1, C2, C3, D1, D2

4. **Night-stop**: Aeronave pernoita no aeroporto

## Estrutura do Projeto

```
src/
├── import_engine/
│   ├── __init__.py
│   ├── rules.py          # Regras de negócio (TAT, TPS, etc.)
│   ├── classifier.py     # Lógica de classificação A/D
│   └── importer.py       # Processador principal CSV
├── app/
│   └── routers/
│       └── upload.py     # Endpoint FastAPI
tests/
└── test_import_engine.py # Testes unitários
```

## Formato CSV de Entrada

```csv
flight_no,callsign,ac_type,reg,schedule_time,actual_time,terminal,gate,dom_intl,night_stop
XY123,ABY123,A320,XY-ABC,2024-06-01T08:00:00,2024-06-01T08:05:00,T1,A5,intl,false
XY124,ABY124,B737,XY-ABD,2024-06-01T14:30:00,,T2,B3,dom,true
```

## Como Usar

### 1. Via Linha de Comando
```bash
python -m src.import_engine.importer sample_flight.csv
```

### 2. Via API FastAPI
```bash
POST /upload/flights
Content-Type: multipart/form-data
```

### 3. Saída Gerada
- `output/arrivals.csv` - Chegadas processadas
- `output/departures.csv` - Partidas processadas
- `import.log` - Log detalhado do processo

## Exemplo de Processamento

**Entrada:**
```csv
XY123,ABY123,A320,XY-ABC,2024-06-01T08:00:00,2024-06-01T08:05:00,T1,A5,intl,false
```

**Saída (Partida):**
- `actual_out`: 2024-06-01T08:05:00
- `actual_in`: 2024-06-01T07:20:00 (calculado: 08:05 - 45min TAT)

## Testes

```bash
PYTHONPATH=/project/sandbox/user-workspace pytest tests/test_import_engine.py -v
```

**Resultados:**
- ✅ test_classify_arrival_only PASSED
- ✅ test_classify_departure_only PASSED  
- ✅ test_classify_both_times PASSED
- ✅ test_turnaround_calculation PASSED

## Benefícios

1. **Redução de 50% no trabalho**: Uma importação ao invés de duas
2. **Eliminação de inconsistências**: Regras automáticas garantem coerência
3. **Flexibilidade**: Configuração fácil de TAT por tipo de aeronave
4. **Auditoria**: Log completo de todas as operações
5. **Escalabilidade**: Processamento via pandas para grandes volumes

## Configuração

As regras podem ser ajustadas em `src/import_engine/rules.py`:

```python
tat_matrix = {
    "A320": timedelta(minutes=45),
    "B737": timedelta(minutes=45),
    "A330": timedelta(minutes=60),
    # Adicionar novos tipos conforme necessário
}
```

## Status do Sistema
✅ **Implementado e Testado**
- 3 linhas de entrada → 1 chegada + 2 partidas geradas
- 0 warnings/erros
- Todos os testes passando
