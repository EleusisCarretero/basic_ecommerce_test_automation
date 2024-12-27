"""
Base test page class
"""
from basic_ecommerce_test_automation.utils.browser_manager import BrowserManager
from basic_ecommerce_test_automation.utils.tools import YamlManager

class BasePageException(Exception):
    """Exception for BasePage class"""
    pass

class BasePage:

    def __init__(self, testing_page, logger_manager, browser, url, *args):
        self._testing_page = YamlManager.get_yaml_file_data(testing_page)
        self.log = logger_manager.get_logger(self.__class__.__name__)
        self.driver_manager = BrowserManager(logger_manager, browser, url,*args)

    @property
    def testing_page(self):
        return self._testing_page
    
    @testing_page.setter
    def testing_page(self, new_value):
        self._testing_page = new_value
