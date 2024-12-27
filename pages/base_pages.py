"""
Base test page class
"""
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class BasePageException(Exception):
    """Exception for BasePage class"""
    pass

class BasePage:

    def __init__(self, browser):
        self.driver = browser.get_driver()
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        

    @property
    def testing_page(self):
        return self._testing_page
    
    @testing_page.setter
    def testing_page(self, new_value):
        self._testing_page = new_value
