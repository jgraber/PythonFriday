import json
import urllib
import subprocess
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

desired_cap = {
  # allowed browsers are `chrome`, `edge`, `playwright-chromium`, 
  # `playwright-firefox` and `playwright-webkit`
  'browser': 'chrome',  
  # this capability is valid only for branded `chrome` and `edge` 
  # browsers and you can specify any browser version like `latest`, 
  # `latest-beta`, `latest-1` and so on.
  'browser_version': 'latest', 
  'os': 'osx',
  'os_version': 'catalina',
  'name': 'Branded Google Chrome on Catalina',
  'build': 'playwright-python-1',
  'browserstack.username': f'{os.getenv("user")}',
  'browserstack.accessKey': f'{os.getenv("accessKey")}'
}

def run_session(playwright):
  version = str(subprocess.getoutput('playwright --version'))
  clientPlaywrightVersion = version.strip().split(" ")[1]
  desired_cap['client.playwrightVersion'] = clientPlaywrightVersion
  cap_quoted = urllib.parse.quote(json.dumps(desired_cap))
  cdpUrl = 'wss://cdp.browserstack.com/playwright?caps=' + cap_quoted
  browser = playwright.chromium.connect(cdpUrl)
  page = browser.new_page()
  try:
    page.goto("https://www.google.co.in/")
    page.fill("[aria-label='Search']", 'Browserstack')
    locator = page.locator("[aria-label='Google Search'] >> nth=0")
    locator.click()
    title = page.title()

    if title == "Browserstack - Google Search":
      # following line of code is responsible for marking the status 
      # of the test on BrowserStack as 'passed'. You can use this code 
      # in your after hook after each test
      mark_test_status("passed", "Title matched", page)
    else:
      mark_test_status("failed", "Title did not match", page)
  except Exception as err:
      mark_test_status("failed", str(err), page)

  browser.close()

def mark_test_status(status, reason, page):
  page.evaluate("_ => {}", 
    "browserstack_executor: {\"action\": \"setSessionStatus\"," + 
    " \"arguments\": {\"status\":\"" + 
    status + "\", \"reason\": \"" + reason + "\"}}");

with sync_playwright() as playwright:
  run_session(playwright)
