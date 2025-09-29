# tests/test_login.py

import pytest
from pages.login_page import LoginPage

@pytest.mark.ui
def test_valid_login_as_impersonate_user(page):
    """Valid login and impersonation using Entity UID."""
    login_page = LoginPage(page)
    login_page.goto("https://dukeport201.t2qa.com/DUKEQA1/adm/users/auth.aspx?from=https://dukeport201.t2qa.com/DUKEQA1/adm/dev/impersonateUser.aspx")
    
    login_page.login("Kasey1", "Parking123!!!")
    login_page.enter_entity_uid("301405")
    
    assert login_page.is_login_successful(), "Impersonation failed: 'Impersonate' text not found"