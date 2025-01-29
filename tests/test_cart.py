"""
Contains the test classes and test methods related to cart validations
"""
import random
import pytest
from pages.checkout_page import CheckOutPage
from ..pages.home_page import HomePage, HomePageException
from ..pages.cart_page import CartPage
from ..pages.product_page import ProductPage
from ..tests.base_test import BaseTest
from ..pages.login_page import LoginPage
from ..utils.tools import YamlManager
from ..utils.browser_manager import BrowserManagerException


@pytest.fixture(scope="session")
def api_settings():
    """
    Fixture to get the instance of ResultManagerClass, common in all tests.
    """
    return YamlManager.get_yaml_file_data("E:/11)_Eleusis_Git_Stuf/basic_ecommerce_test_automation/tests/test_inputs/api_config.yaml")["cart"]


class BaseTestCartError(Exception):
    pass


class BaseTestCart(BaseTest):

    TESTING_PAGE =  "E:/11)_Eleusis_Git_Stuf/basic_ecommerce_test_automation/tests/test_inputs/sauce_demo.yaml"
    def setup(self, browser, result, run_users_api):
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
        self.cart_page = CartPage(
            browser,
            self.TESTING_PAGE
        )
        self.product_page = ProductPage(
            browser,
            self.TESTING_PAGE
        )
        self.checkout_page = CheckOutPage(
            browser,
            self.TESTING_PAGE
        )
        try:
            self.login_page.open_page()
            self.login_page.login_page(**self.login_page.get_just_specific_user("standard_user"))
        except BrowserManagerException as e:
            self.log.error("Unable to login using standard user credentials")
            raise BaseTestCartError("Login has failed") from e
    
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

    def iterate_items_list(self, item_list, callback, msg):
        add_sub = {
            "including": lambda a, b: a + b,
            "removing": lambda a, b: abs(a - b),
        } 
        for idx, item_text in enumerate(item_list):
            current_items_added = callback(item_text)
            inc_dec = idx if msg == "including" else len(item_list) - idx
            self.result.check_equals_to(
                actual_value=current_items_added,
                expected_value=add_sub[msg](inc_dec, 1),
                step_msg=f"Check the quantity of items matches the expected after {msg} {item_text} to the cart")
            assert self.result.step_status

    def step_move_to_cart_page(self):
        """
        Step function to move to checkout page from home page
        """
        self.log.info("Moving to checkout page")
        self.result.check_not_raises_any_given_exception(
            method=self.home_page.move_to_cart_page,
            exceptions=BrowserManagerException,
            step_msg="Check moving to checkout page successfully",
        )
        assert self.result.step_status

    def step_move_to_item_page(self, item_name):
        """
        Step function to validate the movement from home page to item page has been successfully
        """
        self.log.info(f"Clicking on item {item_name} and going to its page")
        self.result.check_not_raises_any_given_exception(
            method= self.home_page.move_item_page,
            exceptions=BrowserManagerException,
            step_msg=f"Check moving to {item_name} page successfully",
            item_name=item_name
        )
        assert self.result.step_status

    def step_move_back_to_page(self):
        """
        Step function to validate the movement from item page to home page has been successfully
        """
        self.log.info("Going back to home page")
        self.result.check_not_raises_any_given_exception(
            method=self.product_page.back_to_home_page,
            exceptions=BrowserManagerException,
            step_msg="Check moving to Home page successfully",
        )
        assert self.result.step_status
    
    def step_move_to_checkout_page(self):
        """
        Step function to validate the movement from cart page to checkout page
        """
        self.result.check_not_raises_any_given_exception(
            method=self.cart_page.move_to_checkout_page,
            exceptions=(BrowserManagerException), 
            step_msg="Check the it is successfully move to checkout page"
        )
        assert self.result.step_status


class TestPositiveFlows(BaseTestCart):
    """
    Test class to validate positive login flows
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, browser, result, run_users_api):
        super().setup(browser, result, run_users_api)

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
        # 1. Add items to the cart
        self.iterate_items_list(items_text, self.step_include_item_in_cart, "including")
        # 2. Reorder items list
        random.shuffle(items_text)
        # 3. Remove item from cart
        self.iterate_items_list(items_text, self.step_remove_item_in_cart, "removing")

    @pytest.mark.parametrize(
            ("items_text"), 
            [
                (["Sauce Labs Backpack"]), 
                (["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]), 
                (["Sauce Labs Onesie","Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]), 
                (["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", "Sauce Labs Backpack", "Sauce Labs Onesie"]), 
            ]
    )
    def test_validate_prices(self, items_text):
        """
        Test case validates the items in the cart page corresponds to the items previously selected, as well as their prices.

        Args:
            items_text(list): List of string with the names of the items to test, added and removed
        """
        # 1 . include itesm to the cart
        self.iterate_items_list(items_text, self.step_include_item_in_cart, "including")
        it_home_page = {key:value for key, value in self.home_page.get_item_prices().items() if key in items_text}
        self.log.info(f"Items included in the cart viewed in the home page: {it_home_page}")
        # 2. Click on cart item
        self.step_move_to_cart_page()
        # 3. Get inventory items included in cart page
        it_cart_page = self.cart_page.get_item_prices()
        # 4. for item_text in items_text:
        self.log.info(f"items included in Cart page: {it_cart_page}")
        # 5. compare the items are the same:
        if len(it_home_page) != len(it_cart_page):
            self.log.error(f"Home page items {len(it_home_page)}: {it_home_page}. Cart page items {len(it_cart_page)}: {it_cart_page}")
            raise BaseTestCartError("The items from home page and cart page are the same quantity")
        for h_name, h_price, in it_home_page.items():
            assert h_price == it_cart_page[h_name], "Wrong price"

    @pytest.mark.parametrize(
            ("item_name"), 
            [
                ("Sauce Labs Backpack"), 
                ("Sauce Labs Bike Light"), 
                ("Sauce Labs Onesie")
            ]
    )
    def test_add_item_in_item_page(self, item_name):
        """
        Validate an item page is reachable from home page and the product is able to be included
        in the cart.

        Args:
            item_name(str): Name of the item from home page.
        """
        # 1. Move to item page.
        self.step_move_to_item_page(item_name)
        # 2. Add item to the cart since item page.
        self.product_page.add_item_to_cart()
        # 3. Get quantity of items in the cart
        self.result.check_equals_to(
            actual_value=self.home_page.get_num_items_in_cart(), 
            expected_value=1, 
            step_msg="Check the number of items matches the expected"
        )
        assert self.result.step_status
        # 4. Move back to home page
        self.step_move_back_to_page()
        # 5. Get price of product
        home_price = self.home_page.get_item_prices()[item_name]
        # 6. Move to checkout page
        self.step_move_to_cart_page()
        # 7. Get price from cart page
        cart_price = self.cart_page.get_item_prices()[item_name]
        self.result.check_equals_to(
            actual_value=cart_price, 
            expected_value=home_price, 
            step_msg="Check the item price form home page and cart page is the same"
        )
        assert self.result.step_status
        # 8. Move to checkout button without error
        self.step_move_to_checkout_page()
        # 9. check and get the user data from API
        user = self.step_execute_api_request(
            url="http://127.0.0.1:5000/users",
            is_random=True
        )[0]
        # 10. fill the checkout info
        self.step_check_execution_events(
            callable_event=self.checkout_page.filed_checkout_info,
            exceptions=BrowserManagerException,
            first_name=user["first_name"], last_name=user["last_name"], postal_code=user["zip_code"]
        )
        # 11. Move to checkout-two page
        self.step_check_execution_events(
            callable_event=self.checkout_page.continue_checkout_step_two,
            exceptions=BrowserManagerException,
        )
        # 12. finish buy
        self.step_check_execution_events(
            callable_event=self.checkout_page.finish_buy,
            exceptions=BrowserManagerException,
        )
