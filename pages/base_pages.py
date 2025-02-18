"""
Base test page class
"""
from typing import Union
from test_utils.logger_manager import LoggerManager
from utils.browser_manager import BrowserManagerException, SelectBy


class BasePageException(Exception):
    """Exception for BasePage class"""


class BasePage:
    """
    This is a basic page class which share all the common and more
    abstract methods for the rest of pages
    Attributes:
        browser (BrowserManager): interface of the browser manager
        log (logger): Logger instance
    """
    page_dict = {}

    def __init__(self,
                 browser):
        self.browser = browser
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self.list_of_items = []

    @property
    def testing_page(self):
        """property method to get value from _testing_page"""
        return self._testing_page

    @testing_page.setter
    def testing_page(self, new_value):
        self._testing_page = new_value

    def _get_element_params(self, key):
        by = self.page_dict[key]["by"]
        ele = self.page_dict[key]["value"]
        return by, ele

    def open_page(self):
        """
        Open browser page give the value from 'testing_page'
        """
        self.browser.open_page(self.testing_page)

    def get_webdriver_element_obj(self,
                                  locator:tuple,
                                  driver=None,
                                  timeout=5):
        """
        Wrapper method to get a webdriver element from browser manager.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.
        
        Returns
            Webdriver obj: Element which matches the given seek parameters
        """
        return self.browser.get_present_element(locator=locator, driver=driver, timeout=timeout)

    def get_webdriver_list_element_obj(self,
                                       locator:tuple,
                                       driver=None):
        """
        Wrapper method to get a webdriver element from browser manager.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.
        
        Returns
            Webdriver obj: Element which matches the given seek parameters
        """
        return self.browser.get_present_list_element(locator=locator, driver=driver)

    def click_on_element(self,
                         locator:tuple,
                         driver=None):
        """
        Wrapper method to click on a webdriver element.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
        """
        self.browser.click_wait_clickable_element(locator=locator, driver=driver)

    def get_text_element(self,
                         locator:tuple,
                         driver=None,
                         timeout=5):
        """
        Wrapper method to get the text from webdriver element.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.

        Returns
            Webdriver obj: Element which matches the given seek parameters
        """
        return self.browser.get_element_text(locator=locator, driver=driver, timeout=timeout)

    def set_element_value(self,
                          locator:tuple,
                          keys_value:str,
                          driver=None,
                          timeout=5):
        """
        Sends a specified text input to a web element using WebDriver.

        This method waits for the element to be present within the specified timeout 
        before sending the provided text.

        Args:
            locator (tuple): The locator (By, value) used to find the web element.
            keys_value (str): The text to be entered into the element.
            driver (webdriver, optional): WebDriver instance. Defaults
            to None, using self.driver if not provided.
            timeout (int or float, optional): Maximum time (in seconds)
            to wait for the element to be present. Defaults to 5.

        Raises:
            TimeoutException: If the element is not found within the given timeout.
            WebDriverException: If sending text to the element fails.

        Returns:
            None
        """
        self.browser.enter_text_to_present_element(
            locator=locator,
            driver=driver,
            keys_value=keys_value,
            timeout=timeout
        )

    def get_current_url(self,
                        switch=False):
        """
        Returns the current window url, switch window if it necessary.

        Args:
            switch(bool): Flag to determinate if switch window.
        
        Returns:
            str: url from current window.
        """
        if switch:
            self.browser.switch_window()
        return self.browser.get_current_driver_url()

    def get_inventory_items(self):
        """
        Gets the list of items from the home page inventory.

        Returns:
            list: List of items which are part of the inventory.
        """
        return self.get_webdriver_list_element_obj(self._get_element_params(key="items_list"))

    def get_item_prices(self):
        """
        It gets the available elements in the page (home, or cath page) with names and prices.

        Returns:
            dict: {name1:price1, name2:price2, }
        """
        prices_dict = {}
        list_of_items = self.list_of_items or self.get_inventory_items()
        for item in list_of_items:
            tmp_price = self.get_text_element(
                self._get_element_params(key="item_price"),
                item
            ).split('\n')[0]
            tmp_name = self.get_text_element(self._get_element_params(key="item_name"), item)
            prices_dict.update({tmp_name:tmp_price})
        return prices_dict


    @staticmethod
    def _convert_text_to_list(text,
                              spliter,
                              ini=0,
                              end=-1):
        return text.split(spliter)[ini:end]

    def select_dropdown(self,
                        method: SelectBy,
                        option_value: Union[int, str],
                        locator: tuple,
                        driver=None):
        """
        Selects an option from a dropdown element.

        Args:
            method (SelectBy): Selection method ("value", "index", "visible_text").
            option_value (str or int): Value to select based on the specified method.
            locator (tuple): Element locator (By, value).
            driver (webdriver, optional): WebDriver instance. Defaults to self.driver if None.

        Raises:
            BasePageException: If the dropdown selection fails.

        Returns:
            bool: True if the selection was successful.
        """
        try:
            return self.browser.select_dropdown_option(method, option_value, locator, driver)
        except BrowserManagerException as e:
            self.log.error(
                f"Unable to select dropdown element using method '{method}' "
                f"with value '{option_value}' and locator {locator}"
            )
            raise BasePageException("Dropdown selection failed") from e
