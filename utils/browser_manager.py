"""
Browser manager class
"""
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from enum import Enum


class AvailableBrowsers(str, Enum):
    CHROME = "Chrome"
    FIREFOX = "Firefox"
    EDGE = "Edge"

    @classmethod
    def get_available_browsers(cls):
        return [browser for browser in cls]


def wait_for_element():
    """
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            driver = kwargs.get("driver")
            timeout = kwargs.get("timeout", 10)
            by = kwargs.get("by")
            value = kwargs.get("value")
            if not (driver and by and value):
                raise ValueError("driver, by, and value must be provided as kwargs.")
            try:
                element = WebDriverWait(driver, timeout).until(
                    EC.visibility_of_element_located((getattr(By, by), value))
                )
                return func(*args, element=element, **kwargs)
            except TimeoutError as e:
                raise BrowserManagerException(
                    f"Timeout of {timeout}s exceeded while locating element: {value}"
                ) from e
        return wrapper
    return decorator


class BrowserManagerException(Exception):
    pass


class BrowserManager:

    def __init__(self, browser=AvailableBrowsers.CHROME, url=None, *args):
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self.driver = self._init_webdriver(browser, *args)
        if url:
            self.open_page(url)


    def _init_webdriver(self, browser, *args):
        if browser not in AvailableBrowsers.get_available_browsers():
            self.log.error(f"Bowser {browser} is not available")
            raise BrowserManagerException(f"Bowser {browser} is not available")
        options = getattr(webdriver, f"{browser}Options")()
        for arg in args:
            options.add_argument(arg)
        try:
            driver = getattr(webdriver, browser)(options)
        except AttributeError as e:
            self.log.error(f"Error webdriver does not have attribute: {browser}")
            raise BrowserManagerException(f"Error webdriver does not have attribute: {browser}") from e
        return driver

    def open_page(self, url):
        try:
            self.driver.get(url)
            self.log.info(f"Opening page: {url}")
        except Exception as e:
            self.log.error(f"Exception occurred: {e}")
            raise BrowserManagerException(f"Error trying to set page {url}") from e

    def _get_webdriver_element_obj(self, driver, by, element):
        return driver.find_element(getattr(By, by), element)

    @wait_for_element()
    def click_located_element(self, element=None, **kwargs):
        """
        Clic en un elemento localizado.
        """
        try:
            element.click()
        except ElementClickInterceptedException as e:
            self.log.error(f"Element {kwargs.get('value')} is not clickable.")
            raise BrowserManagerException("Unable to click on element") from e

    @wait_for_element()
    def get_text_from_element(self, element=None, **kwargs):
        return element.text
    
    @wait_for_element()
    def enter_text_to_element(self, element=None, **kwargs):
        element.clear()
        element.send_keys(kwargs["keys_value"])

        
    @wait_for_element()
    def get_web_element(self, element=None, **kwargs):
        return element

    def get_driver(self):
        return self.driver
    
    def driver_down(self):
        self.driver.quit()
