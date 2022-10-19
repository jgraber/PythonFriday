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


def login(driver):
    # go to statistik page to get correct redirect to login mask
    driver.get(os.getenv('login_page'))

    # fill username field
    username = driver.find_element(
        by=By.ID, 
        value="usernameOrEmail")
    username.send_keys(os.getenv('user'))
    cont = driver.find_element(
        by=By.CLASS_NAME, 
        value="form-button")
    cont.click()
    
    time.sleep(2)

    # fill password field
    password = driver.find_element(
        by=By.ID, 
        value="password")
    password.send_keys(os.getenv('password'))
    submit = driver.find_element(
        by=By.CLASS_NAME, 
        value="form-button")
    submit.click()

    # wait a moment to finish login
    time.sleep(2)


if __name__ == '__main__':
    load_dotenv()
    driver = prepare_browser()
