# -*- coding: utf-8 -*-
from time import sleep
from random import random
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
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://www.nexoos.com.br/investimentos/")
        print('1')
        sleep(20)
        print('2')
        # driver.find_element_by_link_text("Entrar").click()
        # driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Empresa'])[1]/following::img[1]").click()

        # driver.find_element_by_id("lender_email").click()
        # str_email = 'jeanpablosousarabelo@gmail.com'
        # for letra in str_email:
        #     sleep(1*random())
        #     driver.find_element_by_id("lender_email").send_keys(letra)
        # driver.find_element_by_id("lender_password").click()
        # str_password = '9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i'
        # for letra in str_password:
        #     sleep(1*random())
        #     driver.find_element_by_id("lender_password").send_keys(letra)

        # sleep(60)
        # driver.find_element_by_name("commit").click()
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Políticas de Privacidade'])[1]/following::span[1]").click()
        print('3')
        driver.find_element_by_link_text("Visualizar como lista").click()
        print('fim')

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
