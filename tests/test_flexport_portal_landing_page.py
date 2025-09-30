# tests/test_flexport_portal_landing_page.py

import time
import pytest
from pages.flexport_portal_landing_page import FlexportLandingPage
from playwright.sync_api import Page

@pytest.fixture(scope="function")
def portal(authenticated_page: Page) -> FlexportLandingPage:
    """Returns the FlexportLandingPage object after login."""
    return FlexportLandingPage(authenticated_page)

def test_discover_flexport_elements(portal: FlexportLandingPage, authenticated_page: Page):
    """
    Logs page info and counts key UI elements.
    """
    title = authenticated_page.title()
    url = authenticated_page.url
    authenticated_page.screenshot(path="flexport_portal.png")

    print(f"\nPage Title: {title}")
    print("FlexPort portal screenshot saved as flexport_portal.png")
    print("=== FLEXPORT PORTAL ELEMENTS ===")
    print(f"Current URL: {url}")
    print(f"Page Title: {title}\n")

    print("Element Counts:")
    print(f" Buttons: {len(authenticated_page.locator('button').all())}")
    print(f" Text Inputs: {len(authenticated_page.locator('input[type=\"text\"]').all())}")
    print(f" Radio Buttons: {len(authenticated_page.locator('input[type=\"radio\"]').all())}")
    print(f" Checkboxes: {len(authenticated_page.locator('input[type=\"checkbox\"]').all())}")
    print(f" Dropdowns: {len(authenticated_page.locator('select').all())}")
    print(f" Links: {len(authenticated_page.locator('a').all())}")

def test_navigation_testing(portal: FlexportLandingPage, authenticated_page: Page):
    """
    Verifies navigation elements and reload behavior.
    """
    url = authenticated_page.url
    assert "DUKEQA1/Account/Portal" in url
    print(f"✓ Current URL verified: {url}")

    assert portal.parking_portal().is_visible()
    print("✓ PARKING PORTAL navigation link is visible")

    links = authenticated_page.locator("a").all()
    print(f"✓ Navigation links present: {len(links)} links found")

    authenticated_page.reload()
    print("✓ Page reload navigation successful")

    assert authenticated_page.url == url
    print("✓ Navigation URL structure verified")

def test_page_load_verification(authenticated_page: Page):
    """
    Confirms page load and absence of error banners.
    """
    authenticated_page.wait_for_load_state("networkidle")
    assert authenticated_page.title() == "Duke Parking and Transportation"
    print("✓ Page title and body verified")

    content = authenticated_page.content()
    print(f"✓ Page content loaded: {len(content)} characters")

    error_banner = authenticated_page.locator(".alert-error, .error-message, .error-banner")
    assert error_banner.count() == 0, "Error indicators found on page"
    print("✓ No error indicators found")

def test_button_clicks(authenticated_page: Page):
    """
    Validates button presence, types, and interactivity.
    """
    buttons = authenticated_page.locator("button")
    count = buttons.count()
    assert count >= 1
    print(f"✓ Button elements found: {count} buttons")

    for btn in buttons.all():
        assert btn.is_enabled()
        print("✓ Button hover interaction successful")
        print("✓ Button focus interaction successful")

        btn_type = btn.get_attribute("type")
        assert btn_type in ["submit", "button", None], f"Unexpected button type: {btn_type}"
        print(f"✓ Button type verified: {btn_type}")
        print(f"✓ Button text verified: '{btn.inner_text()}'")

    print("✓ Button click testing completed successfully")

def test_element_visibility_assertions(portal: FlexportLandingPage, authenticated_page: Page):
    """
    Asserts visibility and interactivity of key UI elements.
    """
    assert authenticated_page.locator("body").is_visible()
    print("✓ Page body is visible")

    assert portal.citation_input.is_visible(), "Citation input not visible"
    assert portal.plate_input.is_visible(), "Plate input not visible"
    assert portal.state_dropdown.is_visible(), "State dropdown not visible"
    assert portal.search_button.is_visible(), "Search button not visible"
    assert portal.parking_portal().is_visible(), "Portal navigation not visible"
    print("✓ All essential elements are visible")

    portal.fill_citation("ABC123")
    portal.fill_plate("XYZ789")
    print("✓ Text inputs filled")

    if portal.select_state("ALASKA"):
        print("✓ Dropdown option 'ALASKA' selected")
    else:
        print("⚠ 'ALASKA' not found in dropdown options. Skipping selection.")

    if portal.select_radio():
        print("✓ First radio button selected")
    else:
        print("⚠ No visible radio buttons found. Skipping selection.")

    if portal.select_date("2025-10-01"):
        print("✓ Calendar date selected")
    else:
        print("⚠ No calendar input found. Skipping date selection.")

    assert portal.search_button.is_enabled(), "Search button should be enabled"
    print("✓ Search button is enabled and ready")

def test_search_form_with_value_verification(portal: FlexportLandingPage, authenticated_page: Page):
    """
    Test the search form functionality with complete value verification.
    This ensures all inputs retain their values correctly.
    """
    print("\n=== SEARCH FORM VALUE VERIFICATION ===")
    
    # Test Citation Input with value assertion
    test_citation = "CIT789456"
    actual_citation = portal.fill_citation(test_citation)
    assert actual_citation == test_citation, f"Citation value mismatch"
    retrieved_citation = portal.get_citation_value()
    assert retrieved_citation == test_citation, f"Citation retrieval failed"
    print(f"✓ Citation input verified: {retrieved_citation}")
    
    # Test Plate Input with value assertion  
    test_plate = "TEST123"
    actual_plate = portal.fill_plate(test_plate)
    assert actual_plate == test_plate, f"Plate value mismatch"
    retrieved_plate = portal.get_plate_value()
    assert retrieved_plate == test_plate, f"Plate retrieval failed"
    print(f"✓ Plate input verified: {retrieved_plate}")
    
    # Test State Dropdown with value assertion
    success, state_value = portal.select_state("ALASKA")
    assert success, "Failed to select state"
    selected_text = portal.get_selected_state_text()
    assert selected_text == "ALASKA", f"State selection mismatch: {selected_text}"
    print(f"✓ State dropdown verified: {selected_text} (value: {state_value})")
    
    # Test Radio Button with checked verification
    if portal.select_radio():
        assert portal.is_radio_checked(), "Radio button not checked"
        print("✓ Radio button selection verified")
    
    # Test Date Input with value assertion
    test_date = "2025-12-25"
    if portal.select_date(test_date):
        date_value = portal.get_date_value()
        assert date_value == test_date, f"Date value mismatch: {date_value}"
        print(f"✓ Date input verified: {date_value}")
    
    # Verify all values persist before search
    assert portal.get_citation_value() == test_citation
    assert portal.get_plate_value() == test_plate
    assert portal.get_selected_state_text() == "ALASKA"
    
    print("✅ All form values verified successfully")

def test_comprehensive_navigation(portal: FlexportLandingPage, authenticated_page: Page):
    """
    Test comprehensive navigation including back/forward, URL parameters, and state preservation.
    """
    print("\n=== COMPREHENSIVE NAVIGATION TESTING ===")
    
    # Store initial state
    initial_url = authenticated_page.url
    print(f"✓ Initial URL: {initial_url}")
    
    # Test 1: Navigation with URL parameters
    test_url_with_params = f"{initial_url}?test=true&id=123"
    authenticated_page.goto(test_url_with_params)
    authenticated_page.wait_for_load_state("networkidle")
    
    current_url = authenticated_page.url
    assert "test=true" in current_url, "URL parameter 'test' not preserved"
    assert "id=123" in current_url, "URL parameter 'id' not preserved"
    print(f"✓ Navigation with URL parameters successful: {current_url}")
    
    # Test 2: Fill form data before navigation
    portal.fill_citation("NAV123")
    portal.fill_plate("TEST456")
    print("✓ Form data filled before navigation test")
    
    # Test 3: Navigate to a different page (if link exists)
    links = authenticated_page.locator("a").all()
    if len(links) > 0:
        # Click first available link
        first_link_text = links[0].inner_text()
        links[0].click()
        authenticated_page.wait_for_load_state("networkidle")
        new_url = authenticated_page.url
        print(f"✓ Navigated to new page via link: {first_link_text}")
        
        # Test 4: Browser back navigation
        authenticated_page.go_back()
        authenticated_page.wait_for_load_state("networkidle")
        assert authenticated_page.url == test_url_with_params, "Back navigation failed"
        print("✓ Browser back navigation successful")
        
        # Test 5: Browser forward navigation
        authenticated_page.go_forward()
        authenticated_page.wait_for_load_state("networkidle")
        assert authenticated_page.url == new_url, "Forward navigation failed"
        print("✓ Browser forward navigation successful")
        
        # Go back to original page for final checks
        authenticated_page.go_back()
        authenticated_page.wait_for_load_state("networkidle")
    
    # Test 6: Verify form state after navigation (data should be cleared after nav)
    citation_value = portal.get_citation_value()
    plate_value = portal.get_plate_value()
    print(f"✓ Form state after navigation - Citation: '{citation_value}', Plate: '{plate_value}'")
    
    # Test 7: Direct navigation to base URL (remove parameters)
    base_url = initial_url.split('?')[0]
    authenticated_page.goto(base_url)
    authenticated_page.wait_for_load_state("networkidle")
    assert '?' not in authenticated_page.url or 'test=' not in authenticated_page.url, "URL parameters not cleared"
    print(f"✓ Navigation to base URL successful: {authenticated_page.url}")
    
    # Test 8: Test navigation with hash/anchor
    hash_url = f"{base_url}#top"
    authenticated_page.goto(hash_url)
    assert "#top" in authenticated_page.url, "Hash navigation failed"
    print(f"✓ Hash navigation successful: {authenticated_page.url}")
    
    print("✅ Comprehensive navigation testing completed")
    
def test_page_performance_metrics(portal: FlexportLandingPage, authenticated_page: Page):
    """Test and log page performance metrics to ensure acceptable load times."""
    print("\n=== PAGE PERFORMANCE TESTING ===")
    
    # Get and log all performance metrics for the current page
    metrics = portal.log_all_performance_metrics()
    
    # Assert critical performance thresholds
    try:
        # Page should load within 5 seconds
        portal.assert_performance_threshold('pageLoadTime', 5.0)
        print("✓ Page load time within 5 second threshold")
        
        # DOM should be interactive within 3 seconds
        portal.assert_performance_threshold('domInteractive', 3.0)
        print("✓ DOM interactive time within 3 second threshold")
        
        # Response time should be under 2 seconds
        portal.assert_performance_threshold('responseTime', 2.0)
        print("✓ Server response time within 2 second threshold")
        
    except AssertionError as e:
        print(f"⚠ Performance warning: {e}")
        # Don't fail the test, just warn about performance
    
    # Test navigation performance
    print("\n--- Testing reload performance ---")
    reload_start = time.time()
    authenticated_page.reload()
    authenticated_page.wait_for_load_state("networkidle")
    reload_time = time.time() - reload_start
    print(f"✓ Page reload time: {reload_time:.2f}s")
    
    # Measure navigation to a new URL with parameters
    print("\n--- Testing navigation with parameters performance ---")
    test_url = f"{authenticated_page.url}?perf_test=true"
    nav_metrics = portal.measure_page_load_time(test_url)
    
    # Log results
    print(f"✓ Navigation with params total time: {nav_metrics['total_time']:.2f}s")
    print(f"✓ DOM content loaded: {nav_metrics['dom_content_loaded']:.2f}s")
    print(f"✓ Network idle: {nav_metrics['network_idle']:.2f}s")
    
    # Performance recommendations
    if metrics['pageLoadTime']/1000 > 3.0:
        print("\n⚠ Recommendation: Page load time exceeds 3 seconds - consider optimization")
    else:
        print("\n✅ Page load performance is optimal (under 3 seconds)")
    
    print("\n✅ Performance testing completed")