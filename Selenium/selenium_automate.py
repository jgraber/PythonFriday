from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
import logging

logging.getLogger('WDM').setLevel(logging.NOTSET)

# read value for GH_TOKEN key from .evn file
load_dotenv()

# https://github.com/SergeyPirogov/webdriver_manager#gh_token
# ValueError: API Rate limit exceeded. You have to add GH_TOKEN!!!
# service = Service(executable_path="./geckodriver.exe")
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.implicitly_wait(1) # 1 second

driver.get("https://duckduckgo.com/?t=ha&va=j")

print(50 * '=')

# are we on the right page?
title = driver.title
print(title)

print(50 * '=')

# get all H1 elements
headers = driver.find_elements(by=By.TAG_NAME, value="H1")
for header in headers:
    print(f"H1: [{header.text}]")

print(50 * '=')

# search for a single element
logo = driver.find_element(by=By.ID, value="logo_homepage_link")
print(logo.text)
print(logo.get_attribute('href'))

print(50 * '=')

# Check if Selenium throws an exception if search matches multiple elements
try:
    headers = driver.find_element(by=By.TAG_NAME, value="H1")
    print(f"H1: [{headers.text}]")
except Exception as error:
    print(f"{type(error)}: {error}")

print(50 * '=')

search_box = driver.find_element(
    by=By.ID, 
    value="search_form_input_homepage")
search_box.send_keys("Selenium web")

search_button = driver.find_element(
    by=By.ID, 
    value="search_button_homepage")
search_button.click()

title = driver.title
print(title)

print(50 * '=')

results_div = driver.find_element(by=By.CLASS_NAME, value="results")
results = results_div.find_elements(by=By.TAG_NAME, value="h2")

for result in results:
    print(f"* {result.text}")

print(50 * '=')

# scroll to element
more = driver.find_element(by=By.CLASS_NAME, value="result--more")
driver.execute_script("arguments[0].scrollIntoView();", more)
more.click()

# scroll to end
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

print(50 * '=')


time.sleep(15)

driver.quit()