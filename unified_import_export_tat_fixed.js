// NEW UNIFIED IMPORT/EXPORT FUNCTIONS
function unifiedImport(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  const loadingBackup = document.getElementById('loadingBackup');
  const output = document.getElementById('output');
  if (loadingBackup) loadingBackup.style.display = 'block';

  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      let importedData = null;
      let logMessage = `Iniciando importação de ${file.name}...\n`;
      
      if (file.name.endsWith('.json')) {
        const jsonData = JSON.parse(e.target.result);
        if (jsonData.chegadas && Array.isArray(jsonData.chegadas)) {
          importedData = jsonData.chegadas;
        } else if (Array.isArray(jsonData)) {
          importedData = jsonData;
        } else {
          throw new Error('JSON inválido: propriedade "chegadas" não encontrada ou dados não são um array.');
        }
        logMessage += `Arquivo JSON processado: ${importedData.length} registros encontrados.\n`;
      } else if (file.name.endsWith('.csv')) {
        const lines = e.target.result.trim().split(/\r?\n/);
        const headers = lines[0].split(',').map(h => h.trim());
        importedData = lines.slice(1).map(line => {
          const values = line.split(',');
          const obj = {};
          headers.forEach((header, idx) => {
            obj[header] = values[idx] ? values[idx].trim() : '';
          });
          return obj;
        });
        logMessage += `Arquivo CSV processado: ${importedData.length} registros encontrados.\n`;
      } else {
        throw new Error('Formato de arquivo não suportado. Use .json ou .csv');
      }

      let processedCount = 0;
      let generatedCount = 0;

      importedData.forEach(record => {
        const mappedRecord = {
          companhia: record.companhia || record.airline || record.AIRLINE || record.Airline || '',
          cidade: record.cidade || record.destination || record.DESTINATION || record.city || record.CITY || '',
          icao: record.icao || record.ICAO || record.airport_code || '',
          pais: record.pais || record.country || record.COUNTRY || record.Country || '',
          voo: record.voo || record.flight_no || record.flight || record.FLIGHT || record.Flight || '',
          horario: record.horario || record.actual_time || record.time || record.TIME || record.Time || '',
          aeronave: record.aeronave || record.ac_type || record.aircraft || record['A/C'] || record.AC || '',
          status: record.status || record.STATUS || record.Status || 'Scheduled',
          tps: record.tps || record.terminal || record.gate || record.TPS || record.Terminal || '',
          horarioConfirmado: null,
          frequencia: 1,
          dataCadastro: new Date().toISOString()
        };

        if (!mappedRecord.companhia || !mappedRecord.cidade) {
          logMessage += `Registro ignorado - companhia: "${mappedRecord.companhia}", cidade: "${mappedRecord.cidade}"\n`;
          return;
        }

        if (mappedRecord.horario && mappedRecord.horario.includes('T')) {
          const date = new Date(mappedRecord.horario);
          mappedRecord.horario = formatHora(date);
        }

        registrosChegadas.push(mappedRecord);
        processedCount++;

        const departure = generateDeparture(mappedRecord);
        if (departure) {
          registrosPartidas.push(departure);
          generatedCount++;
        }
      });

      logMessage += `Processamento concluído:\n- ${processedCount} chegadas importadas\n- ${generatedCount} partidas geradas automaticamente\n`;
      if (output) output.value = logMessage;

      if (salvarDados()) {
        alert(`Importação realizada com sucesso!\n${processedCount} chegadas e ${generatedCount} partidas processadas.`);
      }
    } catch (error) {
      console.error('Erro na importação dos voos:', error);
      const errorMsg = `Erro na importação: ${error.message}\n`;
      if (output) output.value = errorMsg;
      alert('Erro na importação: ' + (error.message || 'Erro desconhecido.'));
    } finally {
      if (loadingBackup) loadingBackup.style.display = 'none';
      event.target.value = '';
    }
  };

  reader.onerror = function() {
    alert('Erro ao ler o arquivo.');
    if (loadingBackup) loadingBackup.style.display = 'none';
    event.target.value = '';
  };

  reader.readAsText(file);
}

function calculateTAT(icao, aircraft) {
  // Grupos ICAO especiais
  const specialICAOGroups = ['O', 'H', 'V', 'L', 'U', 'G', 'D', 'E', 'F'];
  
  // Aeronaves Narrowbody (corredor único)
  const narrowbodyAircraft = [
    'B722', 'B731', 'B732', 'B733', 'B734', 'B735', 'B736', 'B737', 'B738', 'B739', 'B73X',
    'A318', 'A319', 'A320', 'A321', 'E170', 'E175', 'E190', 'E195', 
    'MD81', 'MD82', 'MD83', 'MD86', 'MD87', 'MD88', 'MD89', 'MD90',
    'AT72', 'AT75', 'AT76', 'AT42', 'AT43', 'AT45', 'AT46',
    'E110', 'E120', 'E135', 'E140', 'E145', 'L410'
  ];
  
  // Verificar se o ICAO pertence ao grupo especial
  const firstChar = icao ? icao.charAt(0).toUpperCase() : '';
  const isSpecialICAO = specialICAOGroups.includes(firstChar);
  
  // Verificar se é aeronave narrowbody
  const aircraftCode = aircraft ? aircraft.toUpperCase() : '';
  const isNarrowbody = narrowbodyAircraft.includes(aircraftCode);
  
  // Aplicar regras de TAT
  if (isSpecialICAO) {
    return isNarrowbody ? 60 : 120; // Narrowbody: 60min, Widebody: 120min
  } else {
    return isNarrowbody ? 120 : 180; // Narrowbody: 120min, Widebody: 180min
  }
}

function generateDeparture(arrival) {
  let departure = Object.assign({}, arrival);
  
  const flightNo = parseInt(arrival.voo, 10);
  if (!isNaN(flightNo)) {
    if (arrival.companhia.toUpperCase().includes('EMIRATES')) {
      const inputTime = prompt(`Informe o horário para o voo de partida referente a ${arrival.voo}: (HH:MM)`, arrival.horario);
      if (!inputTime || !/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(inputTime)) {
        console.warn('Horário inválido para Emirates. O voo de partida não será gerado.');
        return null;
      }
      departure.voo = (flightNo - 1).toString();
      departure.horario = inputTime;
    } else {
      departure.voo = (flightNo + 1).toString();
      
      // Calcular TAT baseado nas regras corretas
      let tatMinutes = calculateTAT(arrival.icao, arrival.aeronave);
      
      if (arrival.horario && /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(arrival.horario)) {
        const [hours, minutes] = arrival.horario.split(':').map(Number);
        const arrivalDate = new Date();
        arrivalDate.setHours(hours, minutes, 0, 0);
        const departureDate = new Date(arrivalDate.getTime() + tatMinutes * 60000);
        departure.horario = formatHora(departureDate);
      }
    }
  } else {
    departure.voo = arrival.voo; 
  }
  
  departure.status = 'Scheduled';
  return departure;
}

function unifiedExport() {
  try {
    const loadingBackup = document.getElementById('loadingBackup');
    const output = document.getElementById('output');
    if (loadingBackup) loadingBackup.style.display = 'block';

    const formatChoice = prompt('Escolha o formato de exportação:\nDigite 1 para JSON\nDigite 2 para CSV', '1');
    let exportContent = '';
    let filename = 'voos_backup';
    let logMessage = 'Iniciando exportação...\n';

    if (formatChoice === '2') {
      const headers = ['companhia', 'voo', 'cidade', 'icao', 'pais', 'horario', 'aeronave', 'status', 'tps', 'tipo'];
      const rows = [headers.join(',')];
      
      registrosChegadas.forEach(flight => {
        const row = headers.map(h => {
          if (h === 'tipo') return 'chegada';
          return (flight[h] || '').toString().replace(/,/g, ';');
        });
        rows.push(row.join(','));
      });
      
      registrosPartidas.forEach(flight => {
        const row = headers.map(h => {
          if (h === 'tipo') return 'partida';
          return (flight[h] || '').toString().replace(/,/g, ';');
        });
        rows.push(row.join(','));
      });
      
      exportContent = rows.join('\n');
      filename += '.csv';
      logMessage += `Exportação CSV: ${registrosChegadas.length} chegadas + ${registrosPartidas.length} partidas\n`;
      downloadFile(exportContent, filename, 'text/csv');
    } else {
      const exportObject = {
        chegadas: registrosChegadas,
        partidas: registrosPartidas,
        dataExport: new Date().toISOString(),
        versao: '1.0'
      };
      exportContent = JSON.stringify(exportObject, null, 2);
      filename += '.json';
      logMessage += `Exportação JSON: ${registrosChegadas.length} chegadas + ${registrosPartidas.length} partidas\n`;
      downloadFile(exportContent, filename, 'application/json');
    }

    logMessage += 'Exportação concluída com sucesso!';
    if (output) output.value = logMessage;
    alert('Exportação realizada com sucesso!');
  } catch (error) {
    console.error('Erro ao exportar voos:', error);
    const errorMsg = `Erro ao exportar voos: ${error.message}\n`;
    if (output) output.value = errorMsg;
    alert('Erro ao exportar voos: ' + (error.message || 'erro desconhecido'));
  } finally {
    const loadingBackup = document.getElementById('loadingBackup');
    if (loadingBackup) loadingBackup.style.display = 'none';
  }
}

function downloadFile(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Setup event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Configure unified import/export buttons
  const btnImportar = document.getElementById('btnImportarVoos');
  const btnExportar = document.getElementById('btnExportarVoos');
  const inputImportar = document.getElementById('inputImportarVoos');
  
  if (btnImportar && inputImportar) {
    btnImportar.addEventListener('click', () => {
      inputImportar.click();
    });
    inputImportar.addEventListener('change', unifiedImport);
  }
  
  if (btnExportar) {
    btnExportar.addEventListener('click', unifiedExport);
  }
});
