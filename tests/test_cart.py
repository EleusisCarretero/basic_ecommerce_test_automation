"""
Contains the test classes and test methods related to cart validations
"""
import time
import pytest
from basic_ecommerce_test_automation.tests.base_test import BaseTest
from basic_ecommerce_test_automation.pages.home_page import HomePage
from basic_ecommerce_test_automation.pages.login_page import LoginPage
from basic_ecommerce_test_automation.utils.tools import YamlManager

class BaseTestCart(BaseTest):

    TESTING_PAGE =  "E:/11)_Eleusis_Git_Stuf/basic_ecommerce_test_automation/tests/test_inputs/sauce_demo.yaml"
    def setup(self, browser, result):
        super().setup(browser, result)
        self.inventory_page_dict = YamlManager.get_yaml_file_data(self.TESTING_PAGE)["general_inputs"]["inventory_page"]
        self.login_page = LoginPage(
            browser,
            self.TESTING_PAGE
        )
        self.home_page = HomePage(
            browser,
            self.TESTING_PAGE
        )

class TestPositiveFlows(BaseTestCart):
    """
    Test class to validate positive login flows
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, browser, result):
        super().setup(browser, result)
        self.login_page.open_page()

    @pytest.mark.parametrize(
            ("items_text"), 
            [
                (["Sauce Labs Backpack"] ), 
                # (["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]), 
            ]
    )
    def test_add_and_remove_items(self, items_text):
        self.login_page.login_page(**self.login_page.get_just_specific_user("standard_user"))
        # 1 add item to the cart
        for item_text in items_text:
            item = self.home_page.get_single_inventory_item(item_text)
            self.home_page.add_item_to_cart(item)
            time.sleep(4)
            self.home_page.remove_item_from_cart(item)
