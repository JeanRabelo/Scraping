from selenium import webdriver
from time import sleep

print(r'jeanpablosousarabelo@gmail.com')
print(r'9@VGn%Pr6!b7bwhXD8UQzih^ynSj!i')

driver = webdriver.Chrome()
driver.get(r'https://www.nexoos.com.br')
driver.implicitly_wait(time_to_wait=100)


sleep(15)


driver.close()
