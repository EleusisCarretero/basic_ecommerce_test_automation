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
