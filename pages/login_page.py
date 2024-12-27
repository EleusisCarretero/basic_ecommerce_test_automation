"""
Login page class
"""

from basic_ecommerce_test_automation.pages.base_pages import BasePage
from basic_ecommerce_test_automation.utils.tools import YamlManager



class LoginPage(BasePage):
    def __init__(self, browser, testing_page):
        super().__init__(browser)
        self._testing_page = YamlManager.get_yaml_file_data(testing_page)["general_inputs"]["login_page"]
        