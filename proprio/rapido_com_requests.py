import csv
import requests

url = r'https://www.bcb.gov.br/api/relatorio/pt-br/contaspub?path=conteudo/txcred/Reports/TaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=RelatorioHist%C3%B3rico%20Posterior%20a%2001/01/2012&parametros=tipoPessoa:1;modalidade:221;periodoInicial:9/13/2019%2012:00:00%20AM;&exportar=CSV&exibeparametros=false'
response = requests.get(url)

print(response.content)
print(type(response.content))

with open('out_2.csv', 'w', newline='') as f:
    writer = csv.writer(f,quotechar = "'", quoting=csv.QUOTE_NONE)
    for line in response.iter_lines():
        writer.writerow(line.decode('utf-8-sig').split(','))
