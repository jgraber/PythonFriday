from playwright.sync_api import Playwright, sync_playwright, expect, Page
from datetime import date, timedelta
import time
import os
from dotenv import load_dotenv

def run(playwright: Playwright, start_day: date) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login(page)
    download_statistics(page, start_day)

    # ---------------------
    context.close()
    browser.close()

def login(page: Page):
    # go to statistik page to get correct redirect to login mask
    page.goto(os.getenv('login_page'))

    # fill username field
    username = page.get_by_label("Email Address or Username")
    username.fill(os.getenv('user'))

    page.get_by_role("button", name="Continue").first.click()
    time.sleep(2)

    # fill password field
    password = page.get_by_label("Password")
    password.fill(os.getenv('password'))

    page.get_by_role("button", name="Log In").click()
    time.sleep(2)

    # select correct part
    page.get_by_role("link", name="Improve & Repeat").click()


def download_statistics(page: Page, start: date):
    end = date.today()
    stats_day = min(start, end)
        
    while stats_day < end:
        download_statistics_for_day(page, stats_day)
        stats_day += timedelta(days=1)


def download_statistics_for_day(page: Page, day: date):
    posts = f"https://wordpress.com/stats/day/posts/improveandrepeat.com?startDate={day}"
    print(posts)
    page.goto(posts)
    
    time.sleep(2)
     
    download = page.get_by_role("button", name="Download data as CSV")
    download.scroll_into_view_if_needed() 
    download.click()


with sync_playwright() as playwright:
    load_dotenv()
    run(playwright, date(2022, 12, 1))
