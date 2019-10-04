# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://www.bcb.gov.br/estatisticas/reporttxjuros?path=conteudo%2Ftxcred%2FReports%2FTaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=Hist%C3%B3rico%20Posterior%20a%2001%2F01%2F2012&exibeparametros=true")
        driver.find_element_by_id("periodoInicial").click()
        Select(driver.find_element_by_id("periodoInicial")).select_by_visible_text("12/09/2019")
        driver.find_element_by_id("modalidade").click()
        Select(driver.find_element_by_id("modalidade")).select_by_visible_text(u"Crédito pessoal não-consignado")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='de 2'])[1]/following::img[6]").click()
        driver.find_element_by_id("modalidade").click()
        Select(driver.find_element_by_id("modalidade")).select_by_visible_text(u"Crédito pessoal não-consignado")
        driver.find_element_by_id("periodoInicial").click()
        Select(driver.find_element_by_id("periodoInicial")).select_by_visible_text("12/09/2019")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='de 2'])[1]/following::img[6]").click()
        driver.find_element_by_id("periodoInicial").click()
        Select(driver.find_element_by_id("periodoInicial")).select_by_visible_text("11/09/2019")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='de 2'])[1]/following::img[6]").click()
        driver.find_element_by_id("periodoInicial").click()
        Select(driver.find_element_by_id("periodoInicial")).select_by_visible_text("10/09/2019")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='de 2'])[1]/following::img[6]").click()
        driver.find_element_by_id("periodoInicial").click()
        Select(driver.find_element_by_id("periodoInicial")).select_by_visible_text("09/09/2019")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='de 2'])[1]/following::img[6]").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
