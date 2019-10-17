import csv
path_file_original = r'C:\Users\jean_\Documents\GitHub\Scraping\proprio\organizador\dados\1-2-2012.csv'
path_file_condensado = r'C:\Users\jean_\Documents\GitHub\Scraping\proprio\organizador\condensado.csv'

with open(path_file_condensado, 'w', newline='') as file_condensado:
    file_condensado_csv = csv.writer(file_condensado, delimiter=';')
    file_condensado_csv.writerow(['Instituição financeira', 'tx a.m.', 'tx a.a.', 'data_i', 'data_f', 'segmento', 'modalidade', 'tipo_encargo', 'nome_do_arquivo'])
    with open(path_file_original,'r', encoding='utf-8') as file_original:
        file_original_csv = csv.reader(file_original, delimiter=',')
        exportar_linha = False
        for row in file_original_csv:
            if exportar_linha and len(row) > 1:
                file_condensado_csv.writerow(row[1:] + [data_i, data_f, segmento, modalidade, tipo_encargo, nome_arquivo])
            if len(row) != 0 and len(row[0]) > 20 and row[0][2] == r'/' and row[0][5] == r'/' and row[0][10:13] == ' a ':
                data_i = row[0][0:10]
                data_f = row[0][-10:]
                segmento = row[1][0:(row[1].find(' - '))]
                modalidade = row[1][(row[1].find(' - ') + 3):-1]
                tipo_encargo = row[2]
                nome_arquivo = path_file_original[(path_file_original.rfind('\\') + 1):-1]
            elif len(row) != 0 and row[0]=='POSICAO':
                exportar_linha = True
