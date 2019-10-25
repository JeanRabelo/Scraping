from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from pprint import pprint
import json
import csv
from time import sleep
from selenium.webdriver import Chrome
import re

URL_FUNDED_LOAN = r'http://www.nexoos.com.br/mkt/lender/funded_loan/'

emprestimos = list()

def carregar_dados(path, coluna):
    with open(path, 'r') as entrada:
        dado = list()
        entrada_csv = csv.reader(entrada, delimiter=';')
        for row in entrada_csv:
            dado.append(row[coluna])
        dado.pop(0)
        return dado

def fazer_login():
    driver = Chrome()
    driver.get(r'https://www.nexoos.com.br/')
    driver.implicitly_wait(time_to_wait=100)
    print('Faça o login com os dados abaixo em até 15 segundos:')
    print('jeanpablosousarabelo@gmail.com')
    print('9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i')
    print(1)
    sleep(15)
    # print(2)
    # driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Políticas de Privacidade'])[1]/following::span[1]").click()
    # print(3)
    # sleep(3)
    # driver.find_element_by_xpath(u'//*[@id="lender_onboarding"]/div/div/div[1]/button/span').click()
    # print(4)
    return driver

cod_emprestimos = carregar_dados('saida_tabelas_completo.csv', 8)
valores_emprestimos = carregar_dados('saida_tabelas_completo.csv', 4)
porcentagem_alcancada_do_emprestimo = carregar_dados('saida_tabelas_completo.csv', 7)

n_emprestimos = len(cod_emprestimos)

driver = fazer_login()
print(5)

tempo_inicio = datetime.now()

for i in range(0,n_emprestimos):
    emprestimo = dict()
    URL_COMPLETO = URL_FUNDED_LOAN + cod_emprestimos[i]
    driver.get(URL_COMPLETO)
    # fazer futuramente: deixar mais eficiente:

    # sleep(4)
    # print('Tentando colocar 100 investidores')
    # driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='R$'])[10]/following::button[1]").click()
    # driver.find_element_by_xpath("(//a[contains(@href, 'javascript:void(0)')])[4]").click()
    # print('pelo jeito funfou')
    # sleep(4)

    emprestimo['valor_do_emprestimo'] = valores_emprestimos[i]
    emprestimo['porcentagem_alcancada_do_emprestimo'] = porcentagem_alcancada_do_emprestimo[i]

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # A linha abaixo não está muito bonita, vamos ver se ela funfa bem...
    emprestimo['sobre_a_empresa'] = soup.find('div', class_="col-md-8 col-md-pull-4").find_all('p')[0].text

    soup_tabela = soup.find('table', attrs={'class':'panel-body table table-bordered'})
    def get_from_tabela(texto):
        try:
            return soup_tabela.find('td', string=texto).parent.find_all('td')[1].text
        except AttributeError:
            return 'AttributeError'

    def get_site_from_tabela(texto):
        try:
            return soup_tabela.find('a', href=re.compile('^' + r'https://www.' + texto + '.com')).text
        except AttributeError:
            return ''

    emprestimo['cnpj'] = get_from_tabela('CNPJ ')
    emprestimo['razao_social'] = get_from_tabela('Razão Social ')
    emprestimo['tipo_de_sociedade'] = get_from_tabela('Tipo de Sociedade ')
    emprestimo['cnae_principal'] = get_from_tabela('CNAE Principal ')
    emprestimo['capital_social'] = get_from_tabela('Capital Social ')
    emprestimo['numero_de_empregados'] = get_from_tabela('Número de Empregados ')
    emprestimo['data_de_fundacao'] = get_from_tabela('Ano de fundação ')
    emprestimo['pagina_web'] = get_from_tabela('Página Web ')
    emprestimo['endereco'] = get_from_tabela('Endereço ')
    emprestimo['avalistas'] = soup.find(string=re.compile('A empresa possui')).replace('\n', '')
    emprestimo['facebook'] = get_site_from_tabela('facebook')
    emprestimo['instagram'] = get_site_from_tabela('instagram')
    emprestimo['linkedin'] = get_site_from_tabela('linkedin')

    soup_tabela_direita = soup.find('div', class_='right-panel-infos')

    emprestimo['juros'] = soup_tabela_direita.find(string='Juros').parent.parent.find_all('span')[-1].text
    emprestimo['prazo'] = soup_tabela_direita.find(string='Prazo').parent.parent.find_all('span')[1].text
    emprestimo['rating'] = soup_tabela_direita.find(string='Risco').parent.parent.find_all('span')[1].text
    emprestimo['quantidade_de_investidores'] = soup_tabela_direita.find(string=re.compile('Investidores\n$'))
    emprestimo['numero_de_investidores'] = int(emprestimo['quantidade_de_investidores'][emprestimo['quantidade_de_investidores'].find('\n')+1:emprestimo['quantidade_de_investidores'].find(' Inv')])
    emprestimo['tempo_para_finalizar'] = soup_tabela_direita.find(string=re.compile('Finaliza em até '))
    emprestimo['motivo'] = soup_tabela_direita.find(string='Motivo').parent.parent.find_all('span')[1].text

    emprestimo['valor_possivel_de_ser_investido'] = list()

    soup_valor_de_investimento = soup.find(id='bid_investment_value').find_all('option')
    for soup_opcao in soup_valor_de_investimento:
        emprestimo['valor_possivel_de_ser_investido'].append(soup_opcao.text)
    emprestimo['valor_possivel_de_ser_investido'].remove('')

    emprestimo['list_investidores'] = list()

    while len(emprestimo['list_investidores']) < emprestimo['numero_de_investidores']:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup_investidores = soup.find(id = 'bids_list_loan_' + cod_emprestimos[i]).find_all('tr', class_='success')
        for soup_investidor in soup_investidores:
            investidor = dict()
            investidor['identificador_do_investidor'] = soup_investidor.find('td', style='text-align: right; ').text
            investidor['valor_da_oferta'] = soup_investidor.find('td', class_='table-loans-colored').text.replace('\xa0\xa0\xa0','')
            investidor['feito_em'] = soup_investidor.find('td', class_='table-loans-not-bold').text
            emprestimo['list_investidores'].append(investidor)
        if len(emprestimo['list_investidores']) < emprestimo['numero_de_investidores']:
            driver.find_element_by_css_selector("li.page-next > a").click()
            # sleep(3)
    emprestimos.append(emprestimo)
    resultado_parcial = open('emprestimos_parciais_ate_o_' + str(len(emprestimos)) + '.json', 'w')
    json.dump(emprestimos, resultado_parcial)
    resultado_parcial.close
    print(str(i + 1) + ' de ' + str(n_emprestimos) + ' emprestimos gravados.')
    porcentagem = float(i + 1)/float(n_emprestimos)
    print("{0:.3%}".format(porcentagem), end='')
    print(' completo', end=' ')
    print('hora estimada de término: ' + str(datetime.now() + (float(n_emprestimos-i)*(datetime.now()-tempo_inicio)/(float(i + 1)))), end=' ')
    print('hora atual: ' + str(datetime.now()))

resultado_completo = open('emprestimos_completo_ate_o_' + str(len(emprestimos)) + '.json', 'w')
json.dump(emprestimos, resultado_completo)
resultado_completo.close
# print('Atencao!!! ainda não estamos pegando todos os investidores')


# deixa aqui, n apaga, não.
# driver.close()
# print('driver fechado')
