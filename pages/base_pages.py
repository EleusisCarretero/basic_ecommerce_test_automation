"""
Base test page class
"""
from basic_ecommerce_test_automation.utils.tools import YamlManager

class BasePageException(Exception):
    """Exception for BasePage class"""
    pass

class BasePage:

    def __init__(self, testing_page):
        self._testing_page = YamlManager.get_yaml_file_data(testing_page)

    @property
    def testing_page(self):
        return self._testing_page
    
    @testing_page.setter
    def testing_page(self, new_value):
        self._testing_page = new_value
