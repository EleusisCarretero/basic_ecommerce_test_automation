"""
Base test page class
"""

class BasePageException(Exception):
    """Exception for BasePage class"""
    pass

class BasePage:

    def __init__(self, testing_page):
        self.testing_page = testing_page

    @property
    def testing_page(self):
        return self.testing_page 
