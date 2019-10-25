import csv

def carregar_ids(path, coluna):
    with open(path, 'r') as entrada:
        cod_emprestimos = list()
        entrada_csv = csv.reader(entrada, delimiter=';')
        for row in entrada_csv:
            cod_emprestimos.append(row[coluna])
        cod_emprestimos.pop(0)
        return cod_emprestimos

cod_emprestimos = carregar_ids('saida_tabelas_completo.csv', 6)

print(cod_emprestimos)
