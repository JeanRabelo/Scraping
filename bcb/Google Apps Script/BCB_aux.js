function informacoes_estaticas(response_next) {
  var data_i = response_next.substring(0,10)
  var data_f = response_next.substring(13,23)
  var next_dash = response_next.search('-')
  var second_comma = nthIndex(response_next,',',2)
  var segmento = response_next.substring(24,next_dash - 1)
  var modalidade = response_next.substring(next_dash + 2,second_comma)
  var next_line_break = response_next.search(/\r\n/g)
  var tipo_encargo = response_next.substring(second_comma + 1, next_line_break)
  
  return [data_i, data_f, segmento, modalidade, tipo_encargo]
}

function preencher_planilha(str_ssId, response_txt){
  var ss = SpreadsheetApp.openById(str_ssId)
  var s_dados = ss.getSheetByName('Dados')
  
  var response_next = response_txt.substring(response_txt.search(/\r\n/g) + 2, response_txt.length)
  var st_inf = informacoes_estaticas(response_next)
    
  var int_inicio_dados = response_next.search('TAXAS_ANUAIS') + 14
  var dados = response_next.substring(int_inicio_dados, response_next.length)
  
  last_row = s_dados.getLastRow()
  
  var dados_restantes = dados
  var i = 0
  
  while (dados_restantes.indexOf(',') !== -1 && i < 200){
    var dados_restantes = preencher_linha(dados_restantes, s_dados, st_inf, last_row + i)
    i++
    }
}

function preencher_linha(dados, s_dados, st_inf, last_row){

  var instit_financ = dados.substring(nthIndex(dados, ',', 1) + 1,nthIndex(dados, ',', 2))
  var tx_am = parseFloat(dados.substring(nthIndex(dados, ',"', 1) + 2,nthIndex(dados, '","', 1)).replace('.','').replace(',','.')) / 100
  
  try {//LEVANDO-SE EM CONTA O ##### DO BTG
    var tx_aa = parseFloat(dados.substring(nthIndex(dados, '","', 1) + 3,dados.search(/\r\n/g)).replace('.','').replace(',','.')) / 100;
  }
  catch(err) {
    var tx_aa = Math.pow((1 + tx_am), 12) - 1;
  }
  
  s_dados.getRange(last_row + 1, 1).setValue(instit_financ)
  with(s_dados.getRange(last_row + 1, 2)){setValue(tx_am); setNumberFormat('0.00%')}
  with(s_dados.getRange(last_row + 1, 3)){setValue(tx_aa); setNumberFormat('0.00%')}
  with(s_dados.getRange(last_row + 1, 4)){setValue(st_inf[0]); setNumberFormat('dd/mm/yyyy')}
  with(s_dados.getRange(last_row + 1, 5)){setValue(st_inf[1]); setNumberFormat('dd/mm/yyyy')}
  s_dados.getRange(last_row + 1, 6).setValue(st_inf[2])
  s_dados.getRange(last_row + 1, 7).setValue(st_inf[3])
  s_dados.getRange(last_row + 1, 8).setValue(st_inf[4])
  
  var dados = dados.substring(dados.search(/\r\n/g) + 2,dados.length)
  
  return dados
}