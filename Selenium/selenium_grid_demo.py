import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# firefox_options = webdriver.FirefoxOptions()
# driver = webdriver.Remote(
#     command_executor='http://localhost:4444',
#     options=firefox_options
# )

edge_options = webdriver.EdgeOptions()
driver = webdriver.Remote(
    command_executor='http://localhost:4444',
    options=edge_options
)

)
driver.get("https://duckduckgo.com/?t=ha&va=j")

# time.sleep(15)

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

results_div = driver.find_element(
    by=By.CLASS_NAME, 
    value="results")
results = results_div.find_elements(
    by=By.TAG_NAME, 
    value="h2")

for result in results:
    print(f"* {result.text}")

time.sleep(15)

driver.quit() 
  
