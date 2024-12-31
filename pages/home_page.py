"""
Home page class
"""
from basic_ecommerce_test_automation.pages.base_pages import BasePage
from basic_ecommerce_test_automation.utils.tools import YamlManager


class HomePageException(Exception):
    """HomePageError"""


class HomePage(BasePage):
    """
    Class to manage all the functionalities related to the Home page.

    Attributes:
        LOGIN_PAGE_DICT (dict): Saves al the needed and/or relevant inputs for Home page
        testing_page (str): Login page path
    """
      
    def __init__(self, browser, testing_page):
        super().__init__(browser)
        self.page_dict = YamlManager.get_yaml_file_data(testing_page)["general_inputs"]["inventory_page"]
        self.testing_page = self.page_dict["path"]

    def click_on_lateral_menu(self):
        """
        Clicks on lateral meu from Home page.

        It calls click_on_element from 'BasePage' to click on an element. _get_element_params
        returns the need parameters, by and value, to get the correct element.
        """
        self.click_on_element(
            *self._get_element_params(
                key="lateral_menu"
            )
        )
    
    def get_lateral_menu_items(self):
        """
        Method to get all the webdriver elements that are part of the lateral menu.

        Returns:
            Webdriver obj: Returns the webdriver element which contains the lateral menu parts.
        """
        return self.get_webdriver_element_obj(*self._get_element_params(key="lateral_menu_items"))
    
    def click_on_logout(self):
        """
        Clicks on the logout button, which is part of the lateral menu.
        """
        all_menu_items = self.get_lateral_menu_items()
        self.click_on_element(*self._get_element_params(key="logout"), all_menu_items)
    
    def get_inventory_items(self):
        return self.get_webdriver_list_element_obj(*self._get_element_params(key="inventory_items"))
    
    def get_single_inventory_item(self, expected_item_text):
        list_of_items = self.get_inventory_items()
        for item in list_of_items:
            item_text = self.get_text_element(*self._get_element_params(key="single_item"), item)
            if expected_item_text == item_text:
                return item
        raise HomePageException(f"Item wasn't found using text {expected_item_text}")

    def add_item_to_cart(self, item):
        self.click_on_element(*self._get_element_params(key="button-item"), item)
