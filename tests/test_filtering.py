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
        assert self.result.step_status

    
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
        """
        Tests the filtering functionality for product sorting.

        This test verifies that applying different sorting filters (High to Low, A to Z, Z to A, Low to High)
        correctly rearranges the product listings. It follows these steps:

        1. Retrieves product names and prices before applying any filter.
        2. Applies the selected filter and verifies it is correctly applied.
        3. Retrieves the product names and prices after filtering.
        4. Compares the displayed sorting order with the expected sorting order based on the applied filter.

        Args:
            filter_applied (FilteringBy): The sorting filter to be applied.

        Assertions:
            - Ensures that the displayed sorted order matches the expected sorted order.
            - Verifies that the test step execution status is successful.
        """
        def sorted_func(filter_type):
            return {
                FilteringBy.HIGH_TO_LOW: lambda item: float(item[1][1:]),
                FilteringBy.A_TO_Z: lambda item: item[0],
                FilteringBy.Z_TO_A: lambda item: item[0],
                FilteringBy.LOW_TO_HIGH: lambda item: float(item[1][1:]),
            }.get(filter_type, None)

        # 1. Read elements, names and prices before filtering
        unsorted_items = self.home_page.get_item_prices()
        self.log.info(f"Items before apply any sort filter: {unsorted_items}")
        # 2. Apply the desired filter
        self.step_verify_filter_applied(expected_filter=filter_applied)
        # 3. Read current element in the home page
        current_sorted_items = self.home_page.get_item_prices()
        self.log.info(f"Items after apply sort filter {filter_applied}: {unsorted_items}")
        # 4. Make compare
        expected_sorted_items = dict(sorted(unsorted_items.items(), key=sorted_func(filter_applied)))
        for expected_key, _ in expected_sorted_items.items():
            self.result.check_equals_to(
                actual_value=current_sorted_items[expected_key], 
                expected_value=expected_sorted_items[expected_key],
                step_msg=f"Check the value items matches withe the expected after applying filter {filter_applied}")
        assert self.result.step_status
