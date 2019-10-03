from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url_bcb = 'https://www.bcb.gov.br/estatisticas/reporttxjuros?path=conteudo%2Ftxcred%2FReports%2FTaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=Hist%C3%B3rico%20Posterior%20a%2001%2F01%2F2012&exibeparametros=true'

driver = webdriver.Chrome()

driver.get(url=url_bcb)

xpath_opcao_correta = '/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[3]/div/dynamic-comp/bcb-report/div/div/div/table/tbody/tr[2]/td[4]/select'

opcao_correta = driver.find_element_by_xpath(xpath_opcao_correta)

opcao_correta.click

# botao = driver.find_element_by_name(name='btnUltimaPagina')
