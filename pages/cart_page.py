"""
Login page class
"""
from basic_ecommerce_test_automation.pages.base_pages import BasePage
from basic_ecommerce_test_automation.utils.tools import YamlManager


class CartPageException(Exception):
    """
    LoginPase error
    """


class CartPage(BasePage):
    """
    Class to manage all the functionalities related to the login page.

    Attributes:
        LOGIN_PAGE_DICT (dict): Saves al the needed and/or relevant inputs for login page
        testing_page (str): Login page path
    """
    def __init__(self, browser, testing_page):
        super().__init__(browser)
        self.page_dict = YamlManager.get_yaml_file_data(testing_page)["general_inputs"]["cart_page"]
        self.testing_page = self.page_dict["path"]
    
    def get_inventory_items(self):
        """
        Gets the list of items from the home page inventory.

        Returns:
            list: List of items which are part of the inventory.
        """
        items_list = self.get_webdriver_element_obj(*self._get_element_params(key="cart_list"))
        return self.get_webdriver_list_element_obj(*self._get_element_params(key="cart_item"), items_list)
    
    def get_item_prices(self):
        prices = {}
        list_of_items = self.get_inventory_items()
        for item in list_of_items:
            tmp_price = self.get_webdriver_element_obj(*self._get_element_params("item_price"), item, 1)
            tmp_name = self.get_webdriver_element_obj(*self._get_element_params("item_name"), item, 1)
            prices.update({tmp_name:tmp_price})
        return prices
