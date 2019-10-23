import json
from pprint import pprint

path_1 = r'Nexoos\JSONs\arquivos\leva_1_emprestimos_parciais_ate_o_410.json'
path_2 = r'Nexoos\JSONs\arquivos\leva_2_emprestimos_parciais_ate_o_113.json'
path_3 = r'Nexoos\JSONs\arquivos\leva_3_emprestimos_parciais_ate_o_575.json'
path_4 = r'Nexoos\JSONs\arquivos\leva_4_emprestimos_parciais_ate_o_65.json'
path_5 = r'Nexoos\JSONs\arquivos\leva_5_emprestimos_parciais_ate_o_119.json'
path_6 = r'Nexoos\JSONs\arquivos\leva_6_emprestimos_parciais_ate_o_147.json'
path_7 = r'Nexoos\JSONs\arquivos\leva_7_emprestimos_parciais_ate_o_552.json'
path_8 = r'Nexoos\JSONs\arquivos\leva_8_emprestimos_completo_ate_o_1.json'
path_completo = r'Nexoos\JSONs\arquivos\completo.json'


arquivo_1 = open(path_1,'r')
arquivo_2 = open(path_2,'r')
arquivo_3 = open(path_3,'r')
arquivo_4 = open(path_4,'r')
arquivo_5 = open(path_5,'r')
arquivo_6 = open(path_6,'r')
arquivo_7 = open(path_7,'r')
arquivo_8 = open(path_8,'r')
arquivo_completo = open(path_completo, 'w')


json_1 = json.load(arquivo_1)
json_2 = json.load(arquivo_2)
json_3 = json.load(arquivo_3)
json_4 = json.load(arquivo_4)
json_5 = json.load(arquivo_5)
json_6 = json.load(arquivo_6)
json_7 = json.load(arquivo_7)
json_8 = json.load(arquivo_8)

json_completo = json_1 + json_2 + json_3 + json_4 + json_5 + json_6 + json_7 + json_8
json.dump(json_completo, arquivo_completo)
