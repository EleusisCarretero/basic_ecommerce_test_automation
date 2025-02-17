from pages.base_pages import BasePageException
from tests.base_test import BaseTest
from utils.browser_manager import BrowserManagerException
from utils.tools import YamlManager
from pages.home_page import FilteringBy, HomePage
from pages.login_page import LoginPage
import pytest

class BaseFilteringError(Exception):
    pass

class TestFiltering(BaseTest):

    TESTING_PAGE =  "tests/test_inputs/sauce_demo.yaml"
    @pytest.fixture(autouse=True)
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
    
    def step_verify_filter_applied(self, expected_filter):

        # Read current filter applied
        current_filter = self.home_page.get_current_filter_applied()
        if current_filter != expected_filter:
            # Apply filter
            self.result.check_not_raises_any_given_exception(
            method=self.home_page.filter_products,
            exceptions=BasePageException, 
            step_msg="Verify The correct filter has been applied",
            filter_option=expected_filter
            )
            assert self.result.step_status
            current_filter = self.home_page.get_current_filter_applied()
        # Compare the values expected vs actual
        self.result.check_equals_to(
            actual_value=current_filter, 
            expected_value=expected_filter,
            step_msg="Verify the current filtering has been updated")

    
    
    @pytest.mark.parametrize(
            ("filter_applied"),
            [
                (FilteringBy.HIGH_TO_LOW),
                (FilteringBy.A_TO_Z),
                (FilteringBy.Z_TO_A),
                (FilteringBy.LOW_TO_HIGH),
            ]
        )
    def test_filtering_products(self, filter_applied):
        self.step_verify_filter_applied(expected_filter=filter_applied)
        print("Wait here")
