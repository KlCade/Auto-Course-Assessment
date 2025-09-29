# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def authenticated_page():
    """Default login fixture using Kasey1."""
    return login_as_user("Kasey1", "Parking123!!!", "301405")

def login_as_user(username: str, password: str, entity_uid: str):
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

        # Login
        page.fill("input#username", username)
        page.fill("input#password", password)
        page.click("button:has-text('Login')")

        # Impersonate
        page.fill("input#EntityUID", entity_uid)
        page.click("button:has-text('Impersonate')")

        # Confirm login success
        assert page.locator("text=Impersonate").is_visible(), f"Login failed for {username}"

        yield page

        context.close()
