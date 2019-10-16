# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
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
        driver.implicitly_wait(time_to_wait=100)
        str_email = 'jeanpablosousarabelo@gmail.com'
        str_password = '9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i'
        print(f'str_email = {str_email}')
        print(f'str_password = {str_password}')
        print('1')
        # sleep(20)
        print('2')
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Políticas de Privacidade'])[1]/following::span[1]").click()
        sleep(2)
        driver.find_element_by_xpath(u'//*[@id="lender_onboarding"]/div/div/div[1]/button/span').click()
        # driver.find_element_by_name('x').click()
        # sleep(40)
        # driver.find_element_by_xpath('/html/body')
        print('3')
        sleep(10)
        driver.find_element_by_xpath("//a[contains(@href, '/mkt/lender/marketplace?view_mode=list')]").click()
        print('Agora está em modo lista')
        # print(driver.find_element_by_xpath('//*[@id="content_paginator_funded"]/div[1]/div[2]/div[2]/table').get_attribute)
        str_html = driver.page_source
        print(BeautifulSoup(str_html))
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
        # driver.find_element_by_xpath("//tr[1]/td/span/a").click()
        # print('5')

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
