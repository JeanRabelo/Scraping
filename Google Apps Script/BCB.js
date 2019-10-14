function bacen_atualizar(){
  var ss_control_panel = SpreadsheetApp.openById('1HRXD_6aFtPcRmyOD0f3s3VwnY72bD7Bb-F6sJQXzFck')
  var s_controle = ss_control_panel.getSheetByName('Controle')
  var rng_px_current = s_controle.getRange('PX').offset(1, 0)
  
  while(!rng_px_current.isBlank()){
    if (rng_px_current.offset(0,1).getValue()=='y'){
      var str_px_current = rng_px_current.getValue()
      
      var str_px_mod_rng_name = (str_px_current + '_mod').toUpperCase()
      var rng_px_mod_current = s_controle.getRange(str_px_mod_rng_name).offset(1, 0)
      
      while (!rng_px_mod_current.isBlank()){
        if (rng_px_mod_current.offset(0, 1).getValue() =='y'){
          var str_px_mod_date_rng_name = (str_px_current + '_' + rng_px_mod_current.getValue() + '_data').toUpperCase()
          var rng_px_mod_date_current = s_controle.getRange(str_px_mod_date_rng_name).offset(1, 0)
          while (!rng_px_mod_date_current.isBlank()){
            if (rng_px_mod_date_current.offset(0, 1).getValue() =='y'){
              var ss_id = rng_px_mod_current.offset(0,3).getValue()
              var px_id = rng_px_current.offset(0,2).getValue()
              var mod_id = rng_px_mod_current.offset(0,2).getValue()
              var data_id = rng_px_mod_date_current.offset(0,2).getValue()
              rng_px_mod_date_current.offset(0,1).setValue('importando...')
              rng_px_mod_date_current.offset(0,1).setValue(importar_csv_bacen(ss_id, px_id, mod_id, data_id))
            }
            rng_px_mod_date_current = rng_px_mod_date_current.offset(1,0)
          }
        }
        var rng_px_mod_current = rng_px_mod_current.offset(1,0)
      }
    }
    var rng_px_current = rng_px_current.offset(1, 0)
  }
}

function importar_csv_bacen(ss_id, px_id, mod_id, data_id) {
  //wait(10000)
  var str_url = 'https://www.bcb.gov.br/api/relatorio/pt-br/contaspub?path=conteudo/txcred/Reports/TaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=RelatorioHist%C3%B3rico%20Posterior%20a%2001/01/2012&parametros=tipoPessoa:' + px_id + ';modalidade:' + mod_id + ';periodoInicial:' + data_id + '%2012:00:00%20AM;&exportar=CSV&exibeparametros=false'
  var response = UrlFetchApp.fetch(str_url)
  
  if (response.getResponseCode() == 200) {
    var response_txt = UrlFetchApp.fetch(str_url).getContentText()
  }
  else {return 'Codigo da resposta = ' + response.getResponseCode();}
  
  preencher_planilha(ss_id, response_txt)
  return 'importado às ' + Date().toString()
}