"""
Broser manager class
"""
from selenium import webdriver
from enum import Enum


class AvailableBrowsers(str, Enum):
    CHROME = "Chrome"
    FIREFOX = "Firefox"
    EDGE = "Edge"

    @classmethod
    def get_available_browsers(cls):
        return [browser for browser in cls]


class BrowserManagerException(Exception):
    pass



class BrowserManager:

    def __init__(self, logger, browser=AvailableBrowsers.CHROME, url=None, *args):
        self.logger = logger.get_logger(self.__class__.__name__)
        self.driver = self._init_webdriver(browser, *args)
        if url:
            self.open_page(url)


    def _init_webdriver(self, browser, *args):
        if browser not in AvailableBrowsers.get_available_browsers():
            self.logger.error(f"Bowser {browser} is not available")
            raise BrowserManagerException(f"Bowser {browser} is not available")
        options = getattr(webdriver, f"{browser}Options")()
        for arg in args:
            options.add_argument(arg)
        try:
            driver = getattr(webdriver, browser)(options)
        except AttributeError as e:
            self.logger.error(f"Error webdriver does not have attribute: {browser}")
            raise BrowserManagerException(f"Error webdriver does not have attribute: {browser}") from e
        return driver

    def open_page(self, url):
        try:
            self.driver.get(url)
            self.logger.info(f"Opening page: {url}")
        except Exception as e:
            self.logger.error(f"Exception occurred: {e}")
            raise BrowserManagerException(f"Error trying to set page {url}") from e
    
    def get_driver(self):
        return self.driver
    
    def driver_down(self):
        self.driver.quit()
        



