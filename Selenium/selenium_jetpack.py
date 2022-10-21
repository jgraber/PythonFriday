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
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()))
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


def download_statistics(driver, start):
    end = date.today()
    stats_day = min(start, end)
        
    while stats_day < end:
        download_statistics_for_day(driver, stats_day)
        stats_day += timedelta(days=1)


def download_statistics_for_day(driver, day):
    posts = f"https://wordpress.com/stats/day/posts/improveandrepeat.com?startDate={day}"
    driver.get(posts)

    time.sleep(2)
    
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    
    download = driver.find_element(
        by=By.CLASS_NAME, 
        value="stats-download-csv")
    download.click()


if __name__ == '__main__':
    load_dotenv()
    driver = prepare_browser()
    login(driver)
    download_statistics(driver, date(2022, 10, 1))
    driver.quit()
