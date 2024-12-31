"""
Base test page class
"""
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class BasePageException(Exception):
    """Exception for BasePage class"""
    pass

class BasePage:
    """
    This is a basic page class which share all the common and more abstract methods for the rest of pages
    Attributes:
        browser (BrowserManager): interface of the browser manager
        log (logger): Logger instance
    """
    page_dict = {}

    def __init__(self, browser):
        self.browser = browser
        self.log = LoggerManager.get_logger(self.__class__.__name__)

    @property
    def testing_page(self):
        """property method to get value from _testing_page"""
        return self._testing_page

    @testing_page.setter
    def testing_page(self, new_value):
        self._testing_page = new_value

    def _get_element_params(self, key):
        by = self.page_dict[key]["by"]
        ele = self.page_dict[key]["value"]
        return by, ele

    def open_page(self):
        """
        Open browser page give the value from 'testing_page'
        """
        self.browser.open_page(self.testing_page)

    def get_webdriver_element_obj(self, by, value, driver=None, timeout=5):
        """
        Wrapper method to get a webdriver element from browser manager.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.
        
        Returns
            Webdriver obj: Element which matches the given seek parameters
        """
        return self.browser.get_present_element(by=by, value=value, driver=driver, timeout=timeout)
        
    def click_on_element(self, by, value, driver=None):
        """
        Wrapper method to click on a webdriver element.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
        """
        self.browser.click_wait_clickable_element(by=by, value=value, driver=driver)
    
    def get_text_element(self, by, value, driver=None, timeout=5):
        """
        Wrapper method to get the text from webdriver element.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.

        Returns
            Webdriver obj: Element which matches the given seek parameters
        """
        return self.browser.get_element_text(by=by, value=value, driver=driver, timeout=timeout)

    def set_element_value(self, by, value, keys_value, driver=None, timeout=5):
        """
        Wrapper method to send a desired text to webdriver element.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.

        """
        self.browser.enter_text_to_present_element(by=by, value=value, driver=driver, keys_value=keys_value, timeout=timeout)

    def get_current_url(self, switch=False):
        """
        Returns the current window url, switch window if it necessary.

        Args:
            switch(bool): Flag to determinate if switch window.
        
        Returns:
            str: url from current window.
        """
        if switch:
            self.browser.switch_window()
        return self.browser.get_current_driver_url()

    @staticmethod
    def _convert_text_to_list(text, spliter, ini=0, end=-1):
        return text.split(spliter)[ini:end]
