from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time

service = Service(executable_path="./geckodriver.exe")
driver = webdriver.Firefox(service=service)
driver.implicitly_wait(1)

driver.get("https://duckduckgo.com/?t=ha&va=j")
title = driver.title
print(title)

time.sleep(5)

driver.quit()