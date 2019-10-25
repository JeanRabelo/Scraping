from bs4 import BeautifulSoup
from pprint import pprint
import json
import csv
from time import sleep
from selenium.webdriver import Chrome
import re

URL_FUNDED_LOAN = r'http://www.nexoos.com.br/mkt/lender/funded_loan/'

def carregar_dados(path, coluna):
    with open(path, 'r') as entrada:
        cod_emprestimos = list()
        entrada_csv = csv.reader(entrada, delimiter=';')
        for row in entrada_csv:
            cod_emprestimos.append(row[coluna])
        cod_emprestimos.pop(0)
        return cod_emprestimos

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

driver = fazer_login()
print(5)
URL_COMPLETO = URL_FUNDED_LOAN + cod_emprestimos[0]
driver.get(URL_COMPLETO)
# sleep(4)
# print('Tentando colocar 100 investidores')
# driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='R$'])[10]/following::button[1]").click()
# driver.find_element_by_xpath("(//a[contains(@href, 'javascript:void(0)')])[4]").click()
# print('pelo jeito funfou')
# sleep(4)

soup = BeautifulSoup(driver.page_source, 'html.parser')
soup_tabela = soup.find('table', attrs={'class':'panel-body table table-bordered'})
def get_from_tabela(texto):
    try:
        return soup_tabela.find('td', string=texto).parent.find_all('td')[1].text
    except AttributeError:
        return 'AttributeError'

cnpj = get_from_tabela('CNPJ ')
print('cnpj = ' + cnpj)
razao_social = get_from_tabela('Razão Social ')
print('razao_social = ' + razao_social)
tipo_de_sociedade = get_from_tabela('Tipo de Sociedade ')
print('tipo_de_sociedade = ' + tipo_de_sociedade)
cnae_principal = get_from_tabela('CNAE Principal ')
print('cnae_principal = ' + cnae_principal)
capital_social = get_from_tabela('Capital Social ')
print('capital_social = ' + capital_social)
numero_de_empregados = get_from_tabela('Número de Empregados ')
print('numero_de_empregados = ' + numero_de_empregados)
data_de_fundacao = get_from_tabela('Ano de fundação ')
print('data_de_fundacao = ' + data_de_fundacao)
pagina_web = get_from_tabela('Página Web ')
print('pagina_web = ' + pagina_web)
endereco = get_from_tabela('Endereço ')
print('endereco = ' + endereco)
avalistas = soup.find(string=re.compile('^\nA empresa possui\n')).replace('\n', '')
print('avalistas = ' + avalistas)

try:
    facebook = soup_tabela.find('a', href=re.compile('^' + r'https://www.facebook.com')).text
except AttributeError:
    facebook = ''
print('facebook = ' + facebook)

soup_tabela_direita = soup.find('div', class_='right-panel-infos')
print(len(soup_tabela_direita.find(string='Juros').parent.parent.find_all('span')))

juros = soup_tabela_direita.find(string='Juros').parent.parent.find_all('span')[-1].text
print('juros = ' + juros)
prazo = soup_tabela_direita.find(string='Prazo').parent.parent.find_all('span')[1].text
print('prazo = ' + prazo)
rating = soup_tabela_direita.find(string='Risco').parent.parent.find_all('span')[1].text
print('rating = ' + rating)
quantidade_de_investidores = soup_tabela_direita.find(string=re.compile('Investidores\n$'))
numero_de_investidores = int(quantidade_de_investidores[quantidade_de_investidores.find('\n')+1:quantidade_de_investidores.find(' Inv')])
print('quantidade_de_investidores = ' + quantidade_de_investidores)
print('numero_de_investidores = ' + str(numero_de_investidores))
tempo_para_finalizar = soup_tabela_direita.find(string=re.compile('Finaliza em até '))
print('tempo_para_finalizar = ' + tempo_para_finalizar)
motivo = soup_tabela_direita.find(string='Motivo').parent.parent.find_all('span')[1].text
print('motivo = ' + motivo)

valor_de_investimento = list()
soup_valor_de_investimento = soup.find(id='bid_investment_value').find_all('option')
for soup_opcao in soup_valor_de_investimento:
    valor_de_investimento.append(soup_opcao.text)
valor_de_investimento.pop(0)
print('valor_de_investimento = ', end='')
print(valor_de_investimento)

list_investidores = list()

while len(list_investidores) < numero_de_investidores:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup_investidores = soup.find(id = 'bids_list_loan_' + cod_emprestimos[0]).find_all('tr', class_='success')
    for soup_investidor in soup_investidores:
        investidor = dict()
        investidor['identificador_do_investidor'] = soup_investidor.find('td', style='text-align: right; ').text
        investidor['valor_da_oferta'] = soup_investidor.find('td', class_='table-loans-colored').text.replace('\xa0\xa0\xa0','')
        investidor['feito_em'] = soup_investidor.find('td', class_='table-loans-not-bold').text
        list_investidores.append(investidor)
    if len(list_investidores) < numero_de_investidores:
        driver.find_element_by_css_selector("li.page-next > a").click()
        # sleep(3)


print('list_investidores = ', end='')
pprint(list_investidores)
print('numero_de_investidores = ' + str(numero_de_investidores))
print('list_investidores = ' + str(len(list_investidores)))
# print('Atencao!!! ainda não estamos pegando todos os investidores')


# deixa aqui, n apaga, não.
# driver.close()
# print('driver fechado')
