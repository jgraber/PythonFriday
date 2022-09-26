from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
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
