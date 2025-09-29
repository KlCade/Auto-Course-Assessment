from playwright.sync_api import Page, Locator

class FlexportLandingPage:
    def __init__(self, page: Page):
        self.page = page
        self.citation_input = page.locator("input[name='CitationNumber'], input#CitationNumber")
        self.plate_input = page.locator("input[name='PlateNumber'], input#PlateNumber")
        self.state_dropdown = page.locator("select#StateId")
        self.search_button = page.locator("button:has-text('Search Citations')")
        self.radio_button = page.locator("input[type='radio']").first
        self.calendar_input = page.locator("input[type='date']")
        self.parking_portal_link = page.locator("a:has-text('Parking Portal')")

    def parking_portal(self) -> Locator:
        return self.parking_portal_link

    def fill_citation(self, value: str):
        self.citation_input.fill(value)

    def fill_plate(self, value: str):
        self.plate_input.fill(value)

    def select_state(self, label: str = "ALASKA"):
        options = self.state_dropdown.locator("option")
        texts = [opt.inner_text().strip() for opt in options.all()]
        if label in texts:
            self.state_dropdown.select_option(label=label)
            return True
        return False

    def select_radio(self):
        if self.radio_button.count() > 0 and self.radio_button.is_visible():
            self.radio_button.check()
            return True
        return False

    def select_date(self, date_str: str = "2025-10-01"):
        if self.calendar_input.count() > 0 and self.calendar_input.is_visible():
            self.calendar_input.fill(date_str)
            return True
        return False