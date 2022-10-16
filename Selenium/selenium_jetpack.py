from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import time
import os
from dotenv import load_dotenv
import logging


def prepare_browser():
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.implicitly_wait(2) # 2 second
    return driver


if __name__ == '__main__':
    load_dotenv()
    driver = prepare_browser()
