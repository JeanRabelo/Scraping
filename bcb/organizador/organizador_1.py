import csv
path_file_original = r'C:\Users\jean_\Documents\GitHub\Scraping\proprio\organizador\dados\1-2-2012.csv'
path_file_condensado = r'C:\Users\jean_\Documents\GitHub\Scraping\proprio\organizador\condensado.csv'

with open(path_file_original,'r', encoding='utf-8') as file:
    # print(file)
    file_csv = csv.reader(file, delimiter=',')
    for row in file_csv:
        char_end = '\n'
        list_adicional = list()
        printar = False
        if len(row) != 0:
            if len(row[0]) > 20:
                if row[0][2] == r'/' and row[0][5] == r'/' and row[0][10:13] == ' a ':
                    char_end = '            <------informacoes\n'
                    data_i = row[0][0:9]
                    data_f = row[0][-10:-1]
                    segmento = row[1][0:(row[1].find(' - '))]
                    modalidade = row[1][(row[1].find(' - ') + 3):-1]
                    tipo_encargo = row[2]
                    nome_arquivo = path_file_original[(path_file_original.rfind('\\') + 1):-1]
                    list_adicional = [data_i, data_f, segmento, modalidade, tipo_encargo, nome_arquivo]
                    print(f'data_i: {data_i} data_f: {data_f} segmento: {segmento} modalidade: {modalidade} tipo_encargo: {tipo_encargo} nome_arquivo: {nome_arquivo}')
            elif row[0] == 'POSICAO':
                char_end = '            <------header\n'
                printar = True
                # list_adicional = ['data_i', 'data_f', 'segmento', 'modalidade', 'tipo_encargo', 'nome_arquivo']
        if printar:
            print(list(row + list_adicional), end = char_end)
