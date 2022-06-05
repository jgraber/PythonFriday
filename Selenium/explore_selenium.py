# pip install selenium
# download Chrome driver and put it next to this file
# or pip install webdriver-manager

import time
from requests import options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import logging

logging.getLogger('WDM').setLevel(logging.NOTSET)
options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(0.5)
driver.get("https://duckduckgo.com/")
title = driver.title
print(title)

search_box = driver.find_element(by=By.ID, value="search_form_input_homepage")
search_box.send_keys("Selenium")

search_button = driver.find_element(by=By.ID, value="search_button_homepage")
search_button.click()

results = driver.find_elements(by=By.TAG_NAME, value="h2")
for result in results:
    try:
        url = result.find_element(by=By.TAG_NAME, value="a")
        print(f"{result.text} - {url.get_attribute('href')}")
    except:
        print(f"{result.text} - [no URL]")

driver.quit()