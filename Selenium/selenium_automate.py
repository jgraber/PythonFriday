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
driver.implicitly_wait(1)

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

