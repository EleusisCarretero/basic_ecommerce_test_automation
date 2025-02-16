from tests.base_test import BaseTest
from utils.browser_manager import BrowserManagerException
from utils.tools import YamlManager
from pages.home_page import FilteringBy, HomePage
from pages.login_page import LoginPage

class BaseFilteringError(Exception):
    pass

class BaseFiltering(BaseTest):

    TESTING_PAGE =  "tests/test_inputs/sauce_demo.yaml"
    def setup(self, browser, result):
        super().setup(browser, result)
        self.inventory_page_dict = YamlManager.get_yaml_file_data(
            self.TESTING_PAGE
        )["general_inputs"]["inventory_page"]
        self.login_page = LoginPage(
            browser,
            self.TESTING_PAGE
        )
        self.home_page = HomePage(
            browser,
            self.TESTING_PAGE
        )
        try:
            self.login_page.open_page()
            self.login_page.login_page(**self.login_page.get_just_specific_user("standard_user"))
        except BrowserManagerException as e:
            self.log.error("Unable to login using standard user credentials")
            raise BaseFilteringError("Login has failed") from e
    
    def test_filtering_products(self):
        self.home_page.filtering_products_by(filtering_by=FilteringBy.HIGH_TO_LOW)
        print("Wait here")
