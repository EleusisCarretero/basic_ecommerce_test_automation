"""
Login page class
"""
from basic_ecommerce_test_automation.pages.base_pages import BasePage
from basic_ecommerce_test_automation.utils.tools import YamlManager


class ProductPageException(Exception):
    """
    LoginPase error
    """


class ProductPage(BasePage):
    """
    Class to manage all the functionalities related to the login page.

    Attributes:
        LOGIN_PAGE_DICT (dict): Saves al the needed and/or relevant inputs for login page
        testing_page (str): Login page path
    """
    def __init__(self, browser, testing_page):
        super().__init__(browser)
        self.page_dict = YamlManager.get_yaml_file_data(testing_page)["general_inputs"]["product_page"]

    def add_item_to_cart(self):
        """
        Method to add item to the cart, from its own page.
        """
        self.click_on_element(*self._get_element_params(key="add_to_cart_button"))
    
    def back_to_home_page(self):
        """
        Method to go back to home page from item page
        """
        self.click_on_element(*self._get_element_params(key="back_to_products"))
