# 🎯 REGRAS DE TAT ENCONTRADAS NO SISTEMA MANUAL

## 📋 **Regras Extraídas do JavaScript (index.html):**

### **1. Classificação por ICAO (Primeiro Caractere):**
- **Grupo ICAO**: ['O', 'H', 'V', 'L', 'U', 'G', 'D', 'E', 'F']

### **2. Classificação de Aeronaves:**

**Narrowbody (Corredor Único):**
```
B722, B731, B732, B733, B734, B735, B736, B737, B738, B739, B73X, 
A318, A319, A320, A321, E170, E175, E190, E195, MD81, MD82, MD83, 
MD86, MD87, MD88, MD89, MD90, AT72, AT75, AT76, AT42, AT43, AT45, 
AT46, E110, E120, E135, E140, E145, L410
```

**Widebody (Dois Corredores):**
- Todas as outras aeronaves não listadas acima

### **3. Regras de TAT (Tempo de Solo):**

| ICAO Grupo | Tipo Aeronave | TAT |
|------------|---------------|-----|
| **O, H, V, L, U, G, D, E, F** | Narrowbody | **60 min** |
| **O, H, V, L, U, G, D, E, F** | Widebody | **120 min** |
| **Outros ICAO** | Narrowbody | **120 min** |
| **Outros ICAO** | Widebody | **180 min** |

### **4. Regra Especial Emirates:**
- **Emirates**: Pop-up manual para inserir horário de partida
- **Número do voo de partida**: Chegada - 1 (ex: chegada 032 → partida 031)

### **5. Regra Geral (Outras Companhias):**
- **Número do voo de partida**: Chegada + 1 (ex: chegada 123 → partida 124)
- **Horário de partida**: Chegada + TAT calculado

## ✅ **Confirmação:**
Estas são as regras EXATAS do seu sistema manual atual!
