import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get('https://www.bcb.gov.br/estatisticas/reporttxjuros?path=conteudo%2Ftxcred%2FReports%2FTaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=Hist%C3%B3rico%20Posterior%20a%2001%2F01%2F2012&exibeparametros=true')
driver.implicitly_wait(time_to_wait=120)

def escolher_modalidade(str_modalidade):
    Select(driver.find_element_by_id("modalidade")).select_by_visible_text(str_modalidade)

# escolher_modalidade(u"Crédito pessoal não-consignado")
escolher_modalidade(u"Cheque especial")

campo_periodoInicial = Select(driver.find_element_by_id("periodoInicial"))

df_datas_site_bcb = pd.DataFrame(columns=['Datas_no_bacen'])

sleep(20)

print('Vai entrar no loop agora')

for opcao in campo_periodoInicial.options:
    str_data_no_bacen = str(opcao.get_attribute('text'))
    df_datas_site_bcb = df_datas_site_bcb.append({'Datas_no_bacen':str_data_no_bacen},ignore_index=True)

print(df_datas_site_bcb)

df_datas_site_bcb.to_csv(r"C:\Users\jean_\Google Drive\1-Análise de mercado\BI\datas_no_bacen.csv")
