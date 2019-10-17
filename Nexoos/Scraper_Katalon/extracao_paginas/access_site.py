from bs4 import BeautifulSoup
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
    print('Faça o login com os dados abaixo em até 10 segundos:')
    print('jeanpablosousarabelo@gmail.com')
    print('9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i')
    print(1)
    sleep(10)
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
print(URL_COMPLETO)
driver.get(URL_COMPLETO)
soup = BeautifulSoup(driver.page_source, 'html.parser')
soup_tabela = soup.find('table', attrs={'class':'panel-body table table-bordered'})
def get_from_tabela(texto):
    try:
        return soup_tabela.find('td', string=texto).parent.find_all('td')[1].text
    except AttributeError:
        return 'AttributeError'

cnpj = get_from_tabela('CNPJ ')
razao_social = get_from_tabela('Razão Social ')
tipo_de_sociedade = get_from_tabela('Tipo de Sociedade ')
cnae_principal = get_from_tabela('CNAE Principal ')
capital_social = get_from_tabela('Capital Social ')
numero_de_empregados = get_from_tabela('Número de Empregados ')
data_de_fundacao = get_from_tabela('Ano de fundação ')
pagina_web = get_from_tabela('Página Web ')
facebook = soup_tabela.find('a', href=re.compile('^' + r'https://www.facebook.com')).text
endereco = get_from_tabela('Endereço ')
avalistas = soup.find(string=re.compile('^\nA empresa possui\n'))

print('cnpj = ' + cnpj)
print('razao_social = ' + razao_social)
print('tipo_de_sociedade = ' + tipo_de_sociedade)
print('cnae_principal = ' + cnae_principal)
print('capital_social = ' + capital_social)
print('numero_de_empregados = ' + numero_de_empregados)
print('data_de_fundacao = ' + data_de_fundacao)
print('pagina_web = ' + pagina_web)
print('facebook = ' + facebook)
print('endereco = ' + endereco)
print('avalistas = ' + avalistas)



# deixa aqui, n apaga, não.
# driver.close()
# print('driver fechado')
