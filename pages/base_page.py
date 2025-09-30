# pages/base_page.py

from playwright.sync_api import Page, Locator
from typing import Optional, Dict
import logging
import time

logger = logging.getLogger(__name__)

class BasePage:
    """Base class for all page objects with common functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000  # 30 seconds default
    
    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """Wait for element to be visible and return it"""
        timeout = timeout or self.timeout
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element
    
    def safe_click(self, selector: str, timeout: Optional[int] = None):
        """Click element with built-in wait"""
        element = self.wait_for_element(selector, timeout)
        element.click()
        logger.info(f"Clicked element: {selector}")
    
    def safe_fill(self, selector: str, value: str, timeout: Optional[int] = None):
        """Fill input with built-in wait"""
        element = self.wait_for_element(selector, timeout)
        element.fill(value)
        logger.info(f"Filled {selector} with value")
    
    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible without throwing exception"""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False
    
    def wait_for_page_load(self):
        """Wait for page to be fully loaded"""
        self.page.wait_for_load_state("networkidle")
    
    def take_screenshot(self, name: str):
        """Take screenshot with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"
        self.page.screenshot(path=filename)
        logger.info(f"Screenshot saved: {filename}")
        return filename
    
    # ===== VALUE ASSERTION METHODS (CRITERIA 8) =====
    def get_input_value(self, selector: str) -> str:
        """Get the current value of an input field"""
        element = self.page.locator(selector)
        return element.input_value()
    
    def assert_input_value(self, selector: str, expected_value: str) -> bool:
        """Assert that an input has the expected value"""
        actual_value = self.get_input_value(selector)
        assert actual_value == expected_value, f"Expected '{expected_value}', got '{actual_value}'"
        return True
    
    def get_selected_option_text(self, selector: str) -> str:
        """Get the text of the currently selected dropdown option"""
        dropdown = self.page.locator(selector)
        selected_option = dropdown.locator("option:checked")
        return selected_option.inner_text() if selected_option.count() > 0 else ""
    
    def get_selected_option_value(self, selector: str) -> str:
        """Get the value of the currently selected dropdown option"""
        dropdown = self.page.locator(selector)
        return dropdown.input_value()
    
    def assert_text_content(self, selector: str, expected_text: str) -> bool:
        """Assert element contains expected text"""
        element = self.page.locator(selector)
        actual_text = element.inner_text()
        assert expected_text in actual_text, f"Text '{expected_text}' not found in '{actual_text}'"
        return True
    
    def get_attribute_value(self, selector: str, attribute: str) -> str:
        """Get an attribute value from an element"""
        element = self.page.locator(selector)
        return element.get_attribute(attribute)
    
    # ===== PERFORMANCE METRICS METHODS =====
    def measure_page_load_time(self, url: str) -> Dict[str, float]:
        """Measure page load performance metrics"""
        start_time = time.time()
        
        # Navigate to URL
        self.page.goto(url)
        
        # Wait for different load states and capture timing
        dom_time = time.time()
        self.page.wait_for_load_state("domcontentloaded")
        dom_loaded_time = time.time() - dom_time
        
        network_time = time.time()
        self.page.wait_for_load_state("networkidle")
        network_idle_time = time.time() - network_time
        
        total_load_time = time.time() - start_time
        
        metrics = {
            'total_time': total_load_time,
            'dom_content_loaded': dom_loaded_time,
            'network_idle': network_idle_time
        }
        
        # Log performance metrics
        logger.info(f"Page load metrics for {url}:")
        logger.info(f"  Total time: {total_load_time:.2f}s")
        logger.info(f"  DOM content loaded: {dom_loaded_time:.2f}s")
        logger.info(f"  Network idle: {network_idle_time:.2f}s")
        
        return metrics
    
    def get_performance_metrics(self) -> Dict:
        """Get browser performance metrics using JavaScript Performance API"""
        metrics = self.page.evaluate("""
            () => {
                const perf = window.performance;
                const timing = perf.timing || {};
                const navigation = perf.getEntriesByType('navigation')[0] || {};
                
                return {
                    'domContentLoaded': navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart || 0,
                    'loadComplete': navigation.loadEventEnd - navigation.loadEventStart || 0,
                    'domInteractive': navigation.domInteractive - navigation.fetchStart || 0,
                    'pageLoadTime': navigation.loadEventEnd - navigation.fetchStart || 0,
                    'responseTime': navigation.responseEnd - navigation.requestStart || 0,
                    'renderTime': navigation.domComplete - navigation.domLoading || 0,
                    'timeToFirstByte': navigation.responseStart - navigation.fetchStart || 0,
                    'dnsLookup': navigation.domainLookupEnd - navigation.domainLookupStart || 0,
                    'tcpConnection': navigation.connectEnd - navigation.connectStart || 0
                };
            }
        """)
        return metrics
    
    def assert_performance_threshold(self, metric_name: str, max_time_seconds: float) -> bool:
        """Assert that a performance metric is within acceptable threshold"""
        metrics = self.get_performance_metrics()
        actual_time = metrics.get(metric_name, 0) / 1000  # Convert ms to seconds
        
        assert actual_time <= max_time_seconds, \
            f"Performance threshold exceeded for {metric_name}: {actual_time:.2f}s > {max_time_seconds}s"
        
        logger.info(f"✓ {metric_name} within threshold: {actual_time:.2f}s <= {max_time_seconds}s")
        return True
    
    def log_all_performance_metrics(self) -> Dict:
        """Get and log all performance metrics in a readable format"""
        metrics = self.get_performance_metrics()
        
        print("\n=== PERFORMANCE METRICS ===")
        print(f"Page Load Time: {metrics['pageLoadTime']/1000:.2f}s")
        print(f"DOM Interactive: {metrics['domInteractive']/1000:.2f}s")
        print(f"DOM Content Loaded: {metrics['domContentLoaded']/1000:.2f}s")
        print(f"Response Time: {metrics['responseTime']/1000:.2f}s")
        print(f"Render Time: {metrics['renderTime']/1000:.2f}s")
        print(f"Time to First Byte: {metrics['timeToFirstByte']/1000:.2f}s")
        print(f"DNS Lookup: {metrics['dnsLookup']:.0f}ms")
        print(f"TCP Connection: {metrics['tcpConnection']:.0f}ms")
        print("===========================\n")
        
        return metrics