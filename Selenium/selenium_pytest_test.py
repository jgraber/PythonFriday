import pytest
from selenium_pytest_fixture import browser


@pytest.mark.usefixtures("browser")
def test_duckduckgo(browser):
    browser.get("https://duckduckgo.com/?t=ha&va=j")
    assert "DuckDuckGo — Privacy, simplified." == browser.title