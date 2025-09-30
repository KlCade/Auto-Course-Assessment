# conftest.py

import pytest
from playwright.sync_api import sync_playwright, Page, BrowserContext
from typing import Generator

@pytest.fixture(scope="function")
def authenticated_page() -> Generator[Page, None, None]:
    """Default login fixture using Kasey1."""
    yield from login_as_user("Kasey1", "Parking123!!!", "301405")

def login_as_user(username: str, password: str, entity_uid: str) -> Generator[Page, None, None]:
    """Reusable login function for impersonating different users."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to impersonation login
        impersonation_url = (
            "https://dukeport201.t2qa.com/DUKEQA1/adm/users/auth.aspx?"
            "from=https://dukeport201.t2qa.com/DUKEQA1/adm/dev/impersonateUser.aspx"
        )
        page.goto(impersonation_url)
        page.wait_for_load_state("networkidle")
        
        # Login using the correct selectors we found
        page.fill("#ctl00_T2Main_txtLogin", username)
        page.fill("#ctl00_T2Main_txtPassword", password)
        page.click("#ctl00_T2Main_cmdLogin")
        
        page.wait_for_load_state("networkidle")
        
        # Impersonate - use the correct selector for EntityUID
        page.fill("#ctl00_T2Main_txtEntityUid", entity_uid)  # Changed from input#EntityUID
        page.click("#ctl00_T2Main_cmdLogin")  # This button is reused for impersonation
        
        page.wait_for_load_state("networkidle")
        
        # Confirm login success - check for dashboard or portal URL
        if "Account/Portal" not in page.url:
            # Wait a bit more and check again
            page.wait_for_timeout(2000)
        
        assert "Account/Portal" in page.url or page.locator("#dashboard").count() > 0, f"Login failed for {username}"
        
        yield page
        
        context.close()
        browser.close()