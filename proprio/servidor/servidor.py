import csv
import requests
import re
import pandas as pd
from time import sleep
import datetime

df_datas = pd.read_csv(r"datas_no_bacen - formato bacen.csv")

n = float(len(df_datas.index))
i = float(0)

for columns, row in df_datas.iterrows():
    sleep(10)
    str_data = str(row['Datas_no_bacen'])
    # escrever a nova url aqui temporariamente
    url = r'https://www.bcb.gov.br/api/relatorio/pt-br/contaspub?path=conteudo/txcred/Reports/TaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=RelatorioHist%C3%B3rico%20Posterior%20a%2001/01/2012&parametros=tipoPessoa:2;modalidade:210;periodoInicial:' + str_data + r'%2012:00:00%20AM;&exportar=CSV&exibeparametros=false'
    # url = r'https://www.bcb.gov.br/api/relatorio/pt-br/contaspub?path=conteudo/txcred/Reports/TaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=RelatorioHist%C3%B3rico%20Posterior%20a%2001/01/2012&parametros=tipoPessoa:1;modalidade:221;periodoInicial:' + str_data + r'%2012:00:00%20AM;&exportar=CSV&exibeparametros=false'
    response = requests.get(url)
    str_filename = str_data.replace(r'/',r'-')
    with open(str_filename + '.csv', 'wb') as f:
        writer = csv.writer(f,quotechar = "'", quoting=csv.QUOTE_ALL)
        for line in response.iter_lines():
            writer.writerow(line.split(',')) #.decode('utf-8')

    with open(str_filename + '.csv', 'r') as f:
        my_csv_text = f.read()

    # substitute
    new_csv_str = re.sub("'", "", my_csv_text)

    # open new file and save
    new_csv_path = str_filename + '.csv' # or whatever path and name you want
    with open(new_csv_path, 'w') as f:
        f.write(new_csv_str)

    i = i + 1
    str_now = str(datetime.datetime.now()-datetime.timedelta(hours=3))
    str_i = str(int(i))
    str_n = str(int(n))
    print(str_now + ' - ' + str_data + '  -  ' + "{0:.5%}".format(i / n) + ' completo. ' + str_i + ' de ' + str_n + ' arquivos baixados')

print('Todos os arquivos foram baixados!')
print('GLORIA A DEUS!!!!')
