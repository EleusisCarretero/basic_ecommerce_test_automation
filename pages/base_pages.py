"""
Base test page class
"""

class BasePageException(Exception):
    """Exception for BasePage class"""
    pass

class BasePage:

    def __init__(self, browser, logger_manager):
        self.driver = browser.get_driver()
        self.log = logger_manager.get_logger(self.__class__.__name__)
        

    @property
    def testing_page(self):
        return self._testing_page
    
    @testing_page.setter
    def testing_page(self, new_value):
        self._testing_page = new_value
