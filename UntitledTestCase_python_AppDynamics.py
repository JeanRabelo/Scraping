# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

print('0')

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome()
        print('1')
        self.driver.implicitly_wait(30)
        print('2')
        self.base_url = "https://www.katalon.com/"
        print('3')
        self.verificationErrors = []
        print('4')
        self.accept_next_alert = True
        print('5')

    def test_app_dynamics_job(self):
        driver = self.driver
        print('6')
        driver.get("https://www.bcb.gov.br/estatisticas/reporttxjuros?path=conteudo%2Ftxcred%2FReports%2FTaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=Hist%C3%B3rico%20Posterior%20a%2001%2F01%2F2012&exibeparametros=true")
        print('7')
        driver.find_element_by_id("periodoInicial").click()
        print('8')
        Select(driver.find_element_by_id("periodoInicial")).select_by_visible_text("12/09/2019")
        print('9')
        driver.find_element_by_id("modalidade").click()
        print('10')
        Select(driver.find_element_by_id("modalidade")).select_by_visible_text(u"Crédito pessoal não-consignado")
        print('11')
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='de 2'])[1]/following::img[6]").click()
        print('12')

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        print('14')
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        print('16')
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            print('17')
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
