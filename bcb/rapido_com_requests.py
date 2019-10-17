import csv
import requests
import re

url = r'https://www.bcb.gov.br/api/relatorio/pt-br/contaspub?path=conteudo/txcred/Reports/TaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=RelatorioHist%C3%B3rico%20Posterior%20a%2001/01/2012&parametros=tipoPessoa:1;modalidade:221;periodoInicial:9/13/2019%2012:00:00%20AM;&exportar=CSV&exibeparametros=false'
response = requests.get(url)

print(response.content)
print(type(response.content))

with open('out_2.csv', 'w', newline='') as f:
    writer = csv.writer(f,quotechar = "'", quoting=csv.QUOTE_ALL)
    for line in response.iter_lines():
        writer.writerow(line.decode('utf-8-sig').split(','))

with open('out_2.csv', 'r') as f:
    my_csv_text = f.read()

# substitute
new_csv_str = re.sub("'", "", my_csv_text)

# open new file and save
new_csv_path = 'out_3.csv' # or whatever path and name you want
with open(new_csv_path, 'w') as f:
    f.write(new_csv_str)
