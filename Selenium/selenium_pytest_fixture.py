import pytest
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import logging

@pytest.fixture()
def browser():
    """Creates a Firefox browser to run your tests"""
    load_dotenv()
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()))
    driver.implicitly_wait(2)

    # runs your test
    yield driver

    driver.close()
