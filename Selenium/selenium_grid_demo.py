import time
from selenium import webdriver
from selenium.webdriver.common.by import By

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Remote(
    command_executor='http://localhost:4444',
    options=firefox_options
)
driver.get("https://duckduckgo.com/?t=ha&va=j")

