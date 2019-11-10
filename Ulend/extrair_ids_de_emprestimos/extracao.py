from selenium import webdriver
from bs4 import BeautifulSoup as BS
from time import sleep
import csv

PATH_OUT = r'C:\Users\jean_\Documents\GitHub\Scraping\Ulend\extrair_ids_de_emprestimos\controle\ids_de_emprestimos.csv'
driver = webdriver.Chrome()
driver.get(r'https://www.ulend.com.br/')
sleep(100)
soup = BS(driver.page_source, 'html.parser')
soup_ids = soup.find_all('img',id='logo-company')
list_ids = []

for soup_id in soup_ids:
    list_ids.append(str(soup_id.get('src')[56:78]))

saida = open(PATH_OUT,'w', newline='')
saida_csv = csv.writer(saida, delimiter=';')

for id in list_ids:
    saida_csv.writerow(id)

saida.close
