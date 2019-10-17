# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import csv
from time import sleep
from selenium import webdriver
import re

str_email = 'jeanpablosousarabelo@gmail.com'
str_password = '9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i'
print(f'str_email = {str_email}')
print(f'str_password = {str_password}')
saida = open('saida_tabelas.csv', 'w')
saida_csv = csv.writer(saida, delimiter=';')
saida_csv.writerow(['nome_empresa', 'prazo', 'rating', 'TIR', 'valor', 'pagina', 'codigo_emprestimo'])

driver = webdriver.Chrome()
driver.get("https://www.nexoos.com.br/investimentos/")
driver.implicitly_wait(time_to_wait=100)
print('1 - entrou no site')
print('digite a senha em 10 seg')
sleep(10)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Políticas de Privacidade'])[1]/following::span[1]").click()
sleep(3)
driver.find_element_by_xpath(u'//*[@id="lender_onboarding"]/div/div/div[1]/button/span').click()
print('2')
sleep(3)
driver.find_element_by_xpath("//a[contains(@href, '/mkt/lender/marketplace?view_mode=list')]").click()
print('Agora está em modo lista')



def importar_tabela(pagina):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabelas = soup.find_all('div', class_='bootstrap-table')
    tabela_antiga_linhas = tabelas[-1].find_all('tr', class_='text-center') #len(tabelas)
    for linha in tabela_antiga_linhas:
        nome_empresa = linha.find('td', class_='company_name').find('a', style='color: black;').text
        prazo = linha.find('td', class_='term').text.replace('\n','')
        rating = linha.find('td', class_='rating-bar').text
        TIR = linha.find('td', class_='tir').text
        valor = linha.find('td', attrs={"data-label": "Valor "}).text
        codigo_emprestimo = linha.get('id')
        saida_csv.writerow([nome_empresa, prazo, rating, TIR, valor, pagina, codigo_emprestimo])

importar_tabela(1)

pagina = 2

while pagina <=199:
    try:
        driver.get(r'https://www.nexoos.com.br/mkt/lender?loans_funded=' + str(pagina) + '&view_mode=list')
    except:
        try:
            sleep(2)
            driver.get(r'https://www.nexoos.com.br/mkt/lender?loans_funded=' + str(pagina) + '&view_mode=list')
        except:
            try:
                sleep(4)
                driver.get(r'https://www.nexoos.com.br/mkt/lender?loans_funded=' + str(pagina) + '&view_mode=list')
            except:
                saida.close

    importar_tabela(pagina)
    print(pagina)
    pagina = pagina + 1

saida.close
# print(soup)

print('Agora vamos sair')
sleep(4)
driver.find_element_by_xpath("//ul/li/a").click()
driver.find_element_by_xpath("//a[contains(@href, '/mkt/lenders/sign_out')]").click()
print('Saímos')
print('fim')
