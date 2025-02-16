"""
Home page class
"""
from enum import Enum
from pages.base_pages import BasePage
from utils.browser_manager import BrowserManagerException
from utils.tools import YamlManager


class FilteringBy(str, Enum):
    A_TO_Z = "Name (A to Z)"
    Z_TO_A = "Name (A to Z)"
    LOW_TO_HIGH = "Price (low to high)"
    HIGH_TO_LOW = "Price (high to low)"


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
        self.page_dict = YamlManager.get_yaml_file_data(
            testing_page
        )["general_inputs"]["inventory_page"]
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

    def get_single_inventory_item(self, expected_item_text):
        """
        Looks into the inventory list based on its text, and gives back the item obj.

        Args:
            expected_item_text(str): expected text item
        
        Returns:
            Webdriver obj: the items which matches the text
        """
        list_of_items = self.get_inventory_items()
        for item in list_of_items:
            name = self.get_text_element(*self._get_element_params(key="item_name"), driver=item)
            if expected_item_text == name:
                return item
        raise HomePageException(f"Item wasn't found using text {expected_item_text}")

    def add_item_to_cart(self, item):
        """
        Adds the given 'item' to the checkout cart by click its 'Add to cart' button.

        Args:
            item(Webdriver obj): ite to add to checkout cart.
        """
        self.click_on_element(*self._get_element_params(key="add_to_cart_button"), item)

    def remove_item_from_cart(self, item):
        """
        Removes the given 'item' from the checkout cart by click its 'Remove' button.

        Args:
            item(Webdriver obj): ite to add to checkout cart.
        """
        self.click_on_element(*self._get_element_params(key="remove_button"), item)

    def get_num_items_in_cart(self):
        """
        Gets the current items included in the cart.

        Returns:
            int: current quantity of items in the cart.
        """
        try:
            q_items = int(
                self.get_text_element(
                    *self._get_element_params(key="cart_icon"),
                    timeout=1))
            self.log.info(f"The cart has currently {q_items} items")
        except BrowserManagerException:
            self.log.info("There is no item added in the cart")
            q_items = 0
        return q_items

    def move_to_cart_page(self):
        """
        Click on cart button to move to 'Cart' page.
        """
        self.click_on_element(*self._get_element_params(key="cart_button"))

    def move_item_page(self, item_name):
        """
        click on a determinate item in home page and goes to the item page.

        Args:
            item_name(str): name of the item we want to move to its page
        """
        item = None
        list_of_items = self.get_inventory_items()
        for item in list_of_items:
            tmp_name = self.get_text_element(*self._get_element_params(key="item_name"), item)
            if tmp_name == item_name:
                break
        if item is not None:
            self.click_on_element(*self._get_element_params(key="item_name"), item)
        else:
            self.log.info(f"Make sure item {item_name} is in home page")
            raise HomePageException(f"Unable to click on {item_name}")
    
    def filtering_products_by(self, filtering_by):

