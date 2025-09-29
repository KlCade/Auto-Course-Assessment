
# pages/login_page.py

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = "#ctl00_T2Main_txtLogin"
        self.password_input = "#ctl00_T2Main_txtPassword"
        self.login_button = "#ctl00_T2Main_cmdLogin"
        self.entity_uid_input = "#ctl00_T2Main_txtEntityUid"
        self.entity_uid_button = "#ctl00_T2Main_cmdLogin"
        self.expected_text = "Impersonate"

    def goto(self, url):
        """Navigate to the login page."""
        self.page.goto(url)

    def login(self, username, password):
        """Enter credentials and submit login form."""
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)
        self.page.wait_for_load_state("networkidle")

    def enter_entity_uid(self, uid):
        """Enter Entity UID and impersonate."""
        self.page.fill(self.entity_uid_input, uid)
        self.page.click(self.entity_uid_button)
        self.page.wait_for_load_state("networkidle")

    
    def is_login_successful(self):
        """Check if dashboard element is visible after impersonation."""
        try:
            self.page.wait_for_selector('xpath=//*[@id="dashboard"]/li/a', timeout=5000)
            return True
        except TimeoutError:
            return False
