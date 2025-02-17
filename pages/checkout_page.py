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
        self.which_checkout_page = 0
    
    @property
    def testing_page(self):
        """property method to get value from _testing_page"""
        return self._testing_page[self.which_checkout_page]

    @testing_page.setter
    def testing_page(self, new_value):
        self._testing_page = new_value

    def continue_checkout_step_two(self):
        """
        Method to move from checkout page to checkout page
        """
        self.click_on_element(*self._get_element_params(key="continue"))
        # move testing page to checkout-step-two.html
        self.which_checkout_page += 1

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
        self.which_checkout_page += 1

    def back_home(self):
        """
        Method to click on back home button
        """
        self.click_on_element(*self._get_element_params(key="back_home"))
        self.which_checkout_page = 0
