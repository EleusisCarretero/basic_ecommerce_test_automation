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

    def __init__(self, logger, browser=AvailableBrowsers.CHROME, path_page=None, *args):
        self.logger = logger.get_logger(self.__class__.__name__)
        self.driver = self._init_webdriver(browser, *args)
        if path_page:
            self.open_page(path_page)


    def _init_webdriver(self, browser, *args):
        if browser not in AvailableBrowsers.get_available_browsers():
            self.logger.error(f"Bowser {browser} is not available")
        options = getattr(webdriver, f"{browser}Options")()
        for arg in args:
            options.add_argument(arg)
        try:
            driver = getattr(webdriver, browser)(options)
        except AttributeError:
            self.logger.error(f"Error webdriver does not have attribute: {browser}")
        return driver

    def open_page(self, path_page):
        try:
            self.driver.get(path_page)
            self.logger.info(f"Opening page: {path_page}")
        except Exception as e:
            self.logger.error(f"Exception occurred: {e}")
            raise BrowserManagerException(f"Error trying to set page {path_page}") from e
        



