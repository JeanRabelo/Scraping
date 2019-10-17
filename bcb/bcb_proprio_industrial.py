import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get('https://www.bcb.gov.br/estatisticas/reporttxjuros?path=conteudo%2Ftxcred%2FReports%2FTaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=Hist%C3%B3rico%20Posterior%20a%2001%2F01%2F2012&exibeparametros=true')
driver.implicitly_wait(time_to_wait=120)

def escolher_modalidade(str_modalidade):
    driver.find_element_by_id("modalidade").click()
    Select(driver.find_element_by_id("modalidade")).select_by_visible_text(str_modalidade)

def baixar_dia(str_dia):
    driver.find_element_by_id("periodoInicial").click()
    Select(driver.find_element_by_id("periodoInicial")).select_by_visible_text(str_dia)
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='de 2'])[1]/following::img[6]").click()
    print('Foi baixado o CSV do dia: ' + str_dia)

escolher_modalidade(u"Crédito pessoal não-consignado")

df_datas = pd.read_csv(r"C:\Users\jean_\Google Drive\1-Análise de mercado\BI\datas_corretas.csv")

for columns, row in df_datas.iterrows():
    baixar_dia(row['Datas'])

print('terminou')
