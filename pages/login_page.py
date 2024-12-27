"""
Login page class
"""

from basic_ecommerce_test_automation.pages.base_pages import BasePage


class LoginPage(BasePage):
    def __init__(self, testing_page, logger, browser):
        super().__init__(testing_page, logger, browser, "https://www.saucedemo.com/", "--start-maximized")