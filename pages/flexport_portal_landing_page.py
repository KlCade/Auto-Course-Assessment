# pages/flexport_portal_landing_page.py

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class FlexportLandingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)  # Initialize BasePage
        self.citation_input = page.locator("input[name='CitationNumber'], input#CitationNumber")
        self.plate_input = page.locator("input[name='PlateNumber'], input#PlateNumber")
        self.state_dropdown = page.locator("select#StateId")
        self.search_button = page.locator("button:has-text('Search Citations')")
        self.radio_button = page.locator("input[type='radio']").first
        self.calendar_input = page.locator("input[type='date']")
        self.parking_portal_link = page.locator("a:has-text('Parking Portal')")

    def parking_portal(self) -> Locator:
        return self.parking_portal_link

    def fill_citation(self, value: str) -> str:
        """Fill citation and verify the value was entered"""
        self.citation_input.fill(value)
        # ASSERT VALUE - Verify the value was entered correctly
        actual_value = self.citation_input.input_value()
        assert actual_value == value, f"Citation not filled correctly: expected '{value}', got '{actual_value}'"
        return actual_value

    def fill_plate(self, value: str) -> str:
        """Fill plate and verify the value was entered"""
        self.plate_input.fill(value)
        # ASSERT VALUE - Verify the value was entered correctly
        actual_value = self.plate_input.input_value()
        assert actual_value == value, f"Plate not filled correctly: expected '{value}', got '{actual_value}'"
        return actual_value

    def select_state(self, label: str = "ALASKA") -> tuple[bool, str]:
        """Select state and return success status and selected value"""
        options = self.state_dropdown.locator("option")
        texts = [opt.inner_text().strip() for opt in options.all()]
        
        if label in texts:
            self.state_dropdown.select_option(label=label)
            # ASSERT VALUE - Get and verify the selected value
            selected_value = self.state_dropdown.input_value()
            selected_text = self.state_dropdown.locator("option:checked").inner_text()
            assert selected_text == label, f"State not selected correctly: expected '{label}', got '{selected_text}'"
            return True, selected_value
        return False, ""

    def select_radio(self) -> bool:
        """Select radio button and verify it's checked"""
        if self.radio_button.count() > 0 and self.radio_button.is_visible():
            self.radio_button.check()
            # ASSERT VALUE - Verify radio is checked
            is_checked = self.radio_button.is_checked()
            assert is_checked, "Radio button not checked after check() operation"
            return True
        return False

    def select_date(self, date_str: str = "2025-10-01") -> bool:
        """Select date and verify the value"""
        if self.calendar_input.count() > 0 and self.calendar_input.is_visible():
            self.calendar_input.fill(date_str)
            # ASSERT VALUE - Verify date was set
            actual_date = self.calendar_input.input_value()
            assert actual_date == date_str, f"Date not set correctly: expected '{date_str}', got '{actual_date}'"
            return True
        return False

    def get_citation_value(self) -> str:
        """Get current citation input value"""
        return self.citation_input.input_value()

    def get_plate_value(self) -> str:
        """Get current plate input value"""
        return self.plate_input.input_value()

    def get_selected_state_text(self) -> str:
        """Get the text of currently selected state"""
        selected_option = self.state_dropdown.locator("option:checked")
        return selected_option.inner_text() if selected_option.count() > 0 else ""

    def get_selected_state_value(self) -> str:
        """Get the value of currently selected state"""
        return self.state_dropdown.input_value()

    def is_radio_checked(self) -> bool:
        """Check if the radio button is selected"""
        return self.radio_button.is_checked() if self.radio_button.count() > 0 else False

    def get_date_value(self) -> str:
        """Get current date input value"""
        return self.calendar_input.input_value() if self.calendar_input.count() > 0 else ""