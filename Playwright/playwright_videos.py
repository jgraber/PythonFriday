from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    context = browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720},
        viewport={"width": 1280, "height": 720}
    )

    page = context.new_page()
    page.goto("https://github.com/")

    title = page.title();
    page.get_by_role("heading", name="Let’s build from here").click()
    page.get_by_placeholder("Email address").click()
    page.get_by_placeholder("Search GitHub").fill("Playwright")
    page.get_by_placeholder("Search GitHub").press("Enter")

    path = page.video.path()
    print(f"video located in: {path}")


    page.screenshot(path="screenshot.png")
    page.screenshot(path="screenshot_full.png", full_page=True)


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
