"""
Contains the test classes and test methods related to cart validations
"""
import random
import pytest
from basic_ecommerce_test_automation.tests.base_test import BaseTest
from basic_ecommerce_test_automation.pages.home_page import HomePage, HomePageException
from basic_ecommerce_test_automation.pages.login_page import LoginPage
from basic_ecommerce_test_automation.utils.tools import YamlManager
from basic_ecommerce_test_automation.utils.browser_manager import BrowserManagerException


class BaseTestCartError(Exception):
    pass


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
    
    def step_check_look_for_item(self, item_name):
        """
        Step function to check the 'item_name' has been successfully added to the cart.

        Args:
            item_name(str): items's name to add.
        
        Returns:
            Webdriver: objet that matches the 'item_name'
        """
        if not isinstance(item_name, str):
            raise BaseTestCartError("Param 'item_name' should be a str")
        self.log.info(f"Check looking for item {item_name} successfully",)
        try:
            item = self.home_page.get_single_inventory_item(item_name)
        except HomePageException as e:
            raise BaseTestCartError("Unable to add item to the cart") from e
        return item

    def step_include_item_in_cart(self, item_name):
        """
        Step to validate that the addition of some item has been successfully.

        Args:
            item_name(str): items's name to add.
        
        Returns:
            int: quantity of items included in the cart after this last one has been added.
        """
        self.log.info(f"trying to add item {item_name} to cart and returning its current num of items")
        item = self.step_check_look_for_item(item_name)
        self.result.check_not_raises_any_given_exception(
            method=self.home_page.add_item_to_cart,
            exceptions=BrowserManagerException,
            step_msg="Check including item to the cart successfully",
            item=item
        )
        assert self.result.step_status
        return self.home_page.get_num_items_in_cart()
    
    def step_remove_item_in_cart(self, item_name):
        """
        Step to validate that the remotion of some item has been successfully.

        Args:
            item_name(str): items's name to add.
        
        Returns:
            int: quantity of items included in the cart after this last one has been added.
        """
        self.log.info(f"trying to add item {item_name} to cart and returning its current num of items")
        item = self.step_check_look_for_item(item_name)
        self.result.check_not_raises_any_given_exception(
            method=self.home_page.remove_item_from_cart,
            exceptions=BrowserManagerException,
            step_msg="Check removing item from the cart successfully",
            item=item
        )
        assert self.result.step_status
        return self.home_page.get_num_items_in_cart()


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
                (["Sauce Labs Backpack"]), 
                (["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]), 
                (["Sauce Labs Onesie","Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]), 
                (["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", "Sauce Labs Backpack", "Sauce Labs Onesie"]), 
            ]
    )
    def test_add_and_remove_items(self, items_text):
        """
        Test case validates adding and removing items, as well as ensure the quantity of items is the expected.

        Args:
            items_text(list): List of string with the names of the items to test, added and removed
        """
        add_sub = {
            "including": lambda a, b: a + b,
            "removing": lambda a, b: abs(a - b),
        }
        def iterate_items_list(item_list, callback, msg):
            
            for idx, item_text in enumerate(item_list):
                current_items_added = callback(item_text)
                inc_dec = idx if msg == "including" else len(item_list) - idx
                self.result.check_equals_to(
                    actual_value=current_items_added,
                    expected_value=add_sub[msg](inc_dec, 1),
                    step_msg=f"Check the quantity of items matches the expected after {msg} {items_text} to the cart")
                assert self.result.step_status

        self.login_page.login_page(**self.login_page.get_just_specific_user("standard_user"))
        # 1. Add items to the cart
        iterate_items_list(items_text, self.step_include_item_in_cart, "including")
        # 2. Reorder items list
        random.shuffle(items_text)
        # 3. Remove item from cart
        iterate_items_list(items_text, self.step_remove_item_in_cart, "removing")
