from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://github.com/")

    title = page.title();
    print(title)

    page.get_by_role("heading", name="Let’s build from here").click()
    
    page.get_by_placeholder("Email address").click()

    page.get_by_placeholder("Search GitHub").fill("Playwright")

    page.get_by_placeholder("Search GitHub").press("Enter")

    page.get_by_role("link", name="Sign in").click()



    page.goto("https://improveandrepeat.com/about/")
    
    text = page.get_by_role("article").inner_text()
    print(text)
    print("\n==================================\n")
    
    text2 = page.get_by_role("article").text_content()
    print(text2)
    print("\n==================================\n")

    all_texts = page.get_by_role("article").all_inner_texts()
    for value in all_texts:
        print(value)



    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
