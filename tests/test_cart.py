"""
Contains the test classes and test methods related to cart validations
"""
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

    def test_add_and_remove_items(self, items):
        # 1 add item to the cart
        