import selenium
import csv
import re
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep

PATH_CONTROLE = r'C:\Users\jean_\Documents\GitHub\Scraping\Nexoos\extrair_emprestimos_novos\controle\controle.csv'
STR_EMAIL = 'jeanpablosousarabelo@gmail.com'
STR_PASSWORD = '9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i'
print(f'STR_EMAIL = {STR_EMAIL}')
print(f'STR_PASSWORD = {STR_PASSWORD}')

arquivo = open(PATH_CONTROLE, 'w', newline='')
controle_csv = csv.writer(arquivo, delimiter=';')

driver = webdriver.Chrome()

driver.get('https://nexoos.com.br')
driver.implicitly_wait(time_to_wait=100)
sleep(30)
# driver.find_element_by_xpath("//a[contains(@href, '/mkt/lender/marketplace?view_mode=list')]").click()

soup = BS(driver.page_source, 'html.parser')

infos = soup.find_all('tr', id=re.compile('^loan_'), class_='text-center')

informacoes = []

for info in infos:
    informacoes.append([info.attrs['id'][5:],
    info.find('a').string,
    info.parent.parent.parent.parent.parent.parent.find('h3', class_='text-center').string.replace('\n','')])

for linha in informacoes:
    if linha[2] != 'Financiadas':
        controle_csv.writerow([linha[0], linha[1]])

arquivo.close()

print('fim do programa')
