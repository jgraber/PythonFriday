from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Start tracing before creating / navigating a page.
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto("https://github.com/")

    title = page.title();
    page.get_by_role("heading", name="Let’s build from here").click()
    page.get_by_placeholder("Email address").click()
    page.get_by_placeholder("Search GitHub").fill("Playwright")
    page.get_by_placeholder("Search GitHub").press("Enter")
    page.get_by_role("link", name="Sign in").click()


    # Stop tracing and export it into a zip archive.
    context.tracing.stop(path = "trace_demo.zip")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
