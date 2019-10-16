# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
import re

str_email = 'jeanpablosousarabelo@gmail.com'
str_password = '9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i'
print(f'str_email = {str_email}')
print(f'str_password = {str_password}')

driver = webdriver.Chrome()
driver.get("https://www.nexoos.com.br/investimentos/")
driver.implicitly_wait(time_to_wait=100)
print('1 - entrou no site')
print('digite a senha em 10 seg')
sleep(10)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Políticas de Privacidade'])[1]/following::span[1]").click()
sleep(2)
driver.find_element_by_xpath(u'//*[@id="lender_onboarding"]/div/div/div[1]/button/span').click()
print('2')
sleep(1)
driver.find_element_by_xpath("//a[contains(@href, '/mkt/lender/marketplace?view_mode=list')]").click()
print('Agora está em modo lista')

# str_html =
soup = BeautifulSoup(driver.page_source, 'html.parser')
# tabela_antiga_linhas = soup.find_all()
tabelas = soup.find_all('div', class_='bootstrap-table')

tabela_antiga_linhas = tabelas[len(tabelas)-1].find_all('tr', class_='text-center')

for linha in tabela_antiga_linhas:
    nome_empresa = linha.find('td', class_='company_name').find('a', style='color: black;').text
    prazo = linha.find('td', class_='term').text.replace('\n','')
    rating = linha.find('td', class_='rating-bar').text
    TIR = linha.find('td', class_='tir').text
    valor = linha.find('td', attrs={"data-label": "Valor "}).text
    print(f'{nome_empresa} {prazo} {rating} {TIR}')

# print(soup)
print('4')
driver.find_element_by_xpath("//tr[1]/td/span/a").click()
print('5')
driver.find_element_by_xpath("//img[@alt='Nexoos']").click()
print('5 - voltei')
driver.find_element_by_xpath("//tr[2]/td/span/a").click()
print('6')
driver.find_element_by_xpath("//img[@alt='Nexoos']").click()
print('6 - voltei')
driver.find_element_by_xpath("//tr[3]/td/span/a").click()
print('7')
driver.find_element_by_xpath("//img[@alt='Nexoos']").click()
print('7 - voltei')
print('Agora vamos sair')
sleep(4)
driver.find_element_by_xpath("//ul/li/a").click()
driver.find_element_by_xpath("//a[contains(@href, '/mkt/lenders/sign_out')]").click()
print('Saímos')
print('fim')
