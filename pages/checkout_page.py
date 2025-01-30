"""
CheckOut page file related to class
"""
from pages.base_pages import BasePage
from utils.tools import YamlManager


class CheckOutPageException(Exception):
    """
    LoginPase error
    """


class CheckOutPage(BasePage):
    """
    Class to manage all the functionalities related to the login page.

    Attributes:
        LOGIN_PAGE_DICT (dict): Saves al the needed and/or relevant inputs for login page
        testing_page (str): Login page path
    """
    def __init__(self, browser, testing_page):
        super().__init__(browser)
        self.page_dict = YamlManager.get_yaml_file_data(
            testing_page
        )["general_inputs"]["checkout_page"]
        self.testing_page = self.page_dict["path"]

    def continue_checkout_step_two(self):
        """
        Method to move from checkout page to checkout page
        """
        self.click_on_element(*self._get_element_params(key="continue"))

    def filed_checkout_info(self, **kwargs):
        """
        Method to fill the different user data in the checkout page.

        Args:
            **kwargs: fields and data
        """
        for key, value in kwargs.items():
            self.fill_sing_checkout_info_element(key, value)

    def fill_sing_checkout_info_element(self, locator, data_write):
        """
        Method to fill an specific field from the user data in checkout page.

        Args:
            locator(Tuple): Element locator
            data_write(str): user data to be written
        """
        self.set_element_value(*self._get_element_params(key=locator), data_write)

    def finish_buy(self):
        """
        Method to click on finish button
        """
        self.click_on_element(*self._get_element_params(key="finish"))

    def back_home(self):
        """
        Method to click on back home button
        """
        self.click_on_element(*self._get_element_params(key="back_home"))
