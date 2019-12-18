import csv
from selenium import webdriver
from time import sleep
import pyautogui


# PATH_CONTROLE = r'C:\Users\jean_\Documents\GitHub\Scraping\Nexoos\extrair_emprestimos_novos\controle\controle.csv'
PATH_CONTROLE = r'/home/jean/github/Scraping/Nexoos/extrair_emprestimos_novos/controle/controle.csv'
STR_EMAIL = 'jeanpablosousarabelo@gmail.com'
STR_PASSWORD = '9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i'
print(f'STR_EMAIL = {STR_EMAIL}')
print(f'STR_PASSWORD = {STR_PASSWORD}')

arquivo = open(PATH_CONTROLE, 'r')
controle_csv = csv.reader(arquivo, delimiter=';')

driver = webdriver.Chrome()

driver.get('https://nexoos.com.br')
driver.implicitly_wait(time_to_wait=100)
sleep(30)

for line in controle_csv:
    str_loan_id = str(line[0])
    driver.execute_script("window.open('" + 'https://www.nexoos.com.br/mkt/lender/loan/' + str_loan_id + "');")
    # driver.get('' + str_loan_id)
    sleep(4)
    pyautogui.hotkey('ctrl', 's')
    sleep(3)
    pyautogui.typewrite('loan_' + str_loan_id + '.html')
    pyautogui.press('enter')


arquivo.close()

print('fim do programa')
