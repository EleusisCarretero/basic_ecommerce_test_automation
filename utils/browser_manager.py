"""
Browser manager class
"""
from typing import Union
from enum import Enum
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class AvailableBrowsers(str, Enum):
    """
    Enum class to control available browsers
    """
    CHROME = "Chrome"
    FIREFOX = "Firefox"
    EDGE = "Edge"

    @classmethod
    def get_available_browsers(cls):
        """
        Returns a list with al class elements.
        """
        return [browser for browser in cls]


class BrowserManagerException(Exception):
    """BrowserManager Exception class"""


class BrowserManager:
    """
    Class to manage with the webdriver instance.

    Attributes:
        log (logger): Logger instance.
        driver(Webdriver): Webdriver instance.
    """

    def __init__(self, *args, browser=AvailableBrowsers.CHROME, url=None):
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self._driver = self._init_webdriver(browser, *args)
        if url:
            self.open_page(url)

    def _init_webdriver(self, browser, *args):
        if browser not in AvailableBrowsers.get_available_browsers():
            self.log.error(f"Bowser {browser} is not available")
            raise BrowserManagerException(f"Bowser {browser} is not available")
        options = getattr(webdriver, f"{browser}Options")()
        for arg in args:
            options.add_argument(arg)
        try:
            driver = getattr(webdriver, browser)(options)
        except AttributeError as e:
            self.log.error(f"Error webdriver does not have attribute: {browser}")
            raise BrowserManagerException(f"Error webdriver does not have attribute: {browser}") from e
        return driver
    
    @property
    def driver(self):
        """Property method to get _driver value"""
        return self._driver
    
    @driver.setter
    def driver(self, new_driver):
        self._driver = new_driver

    def open_page(self, url:str, driver=None) -> None:
        """
        Opens the url from web page.

        Args:
            url(str): url from webpage.
            driver:(webdriver obj:Optional, Default=None): webdriver object.

        Raises:
            BrowserManagerException: If driver is unable to open url.
        """
        driver = driver or self.driver
        try:
            self.driver.get(url)
            self.log.info(f"Opening page: {url}")
        except Exception as e:
            self.log.error(f"Exception occurred: {e}")
            raise BrowserManagerException(f"Error trying to set page {url}") from e

    def get_webdriver_element_obj(self, driver, by, value):
        """
        Looks for an element, in driver, witch matches with the given by and value.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.

        Returns:
            Element: element with matches the specifications.

        Raises:
            BrowserManagerException: In case there is no element in driver witch matches.
        """
        driver = driver or self.driver
        try:
            return driver.find_element(getattr(By, by), value)
        except NoSuchElementException as e:
            self.log.error(f"Unable to find element with parameters ('{by}', '{value}')")
            raise BrowserManagerException("Unable to find element") from e

    def click_wait_clickable_element(self, by:By, value:str, driver=None, timeout: Union[int, float]=10):
        """
        Waits until the element which matches with the 'by' and ' value' within a timeout and clicks on it, otherwise
        the BrowserManagerException is raised.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.

        Raises:
            BrowserManagerException: In case the timeout has been reached and the element is still not clickable.
        """
        driver = driver or self.driver
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((getattr(By, by), value))
            )
        except TimeoutException as e:
            self.log.error(f"Unable to have element '({by}, {value})' clickable within {timeout}s")
            raise BrowserManagerException("Unable to get element clickable") from e
        element.click()

    def get_present_element(self, by:By, value:str, driver, timeout: Union[int, float]):
        """
        Waits until the element which matches with the 'by' and ' value' within a timeout, (it does not means it is visible)
        otherwise the BrowserManagerException is raised.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.

        Returns:
            Element: Element found which matches within timeout.

        Raises:
            BrowserManagerException: In case the timeout has been reached and the element is still not present.
        """
        driver = driver or self.driver
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((getattr(By, by), value))
            )
        except TimeoutException as e:
            self.log.error(f"Unable get the element using parameters '({by}, {value})' within {timeout}s")
            raise BrowserManagerException("Unable to write on element") from e

    def get_present_list_element(self, by:By, value:str, driver):
        """
        Waits until the element which matches with the 'by' and ' value' within a timeout, (it does not means it is visible)
        otherwise the BrowserManagerException is raised.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.

        Returns:
            Element: Element found which matches within timeout.

        Raises:
            BrowserManagerException: In case the timeout has been reached and the element is still not present.
        """
        driver = driver or self.driver
        try:
            return driver.find_elements(getattr(By, by), value)
        except TimeoutException as e:
            self.log.error(f"Unable get the element using parameters '({by}, {value})'")
            raise BrowserManagerException("Unable to write on element") from e

    def get_visible_element(self, by:By, value:str, driver, timeout: Union[int, float]):
        """
        Waits until the element which matches with the 'by' and ' value' within a timeout, (the element should be visible)
        otherwise the BrowserManagerException is raised.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.

        Returns:
            Element: Element found which matches within timeout.

        Raises:
            BrowserManagerException: In case the timeout has been reached and the element is still not visible.
        """
        driver = driver or self.driver
        try:
            return WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((getattr(By, by), value))
            )
        except TimeoutException as e:
            self.log.error(f"Unable get the element using parameters '({by}, {value})' within {timeout}s")
            raise BrowserManagerException("Unable to write on element") from e

    def enter_text_to_present_element(self, by:By, value:str, keys_value:str, driver, timeout: Union[int, float]) -> None:
        """
        Writes a text ('keys_value') the located element, not necessary visible, with the 'by' and ' value' within a timeout, otherwise
        the BrowserManagerException is raised.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.
        """
        element = self.get_present_element(by, value, driver, timeout)
        element.clear()
        element.send_keys(keys_value)

    def get_element_text(self, by:By, value:str, driver, timeout: Union[int, float], visible=True) -> str:
        """
        Gets the text from an element.

        Args:
            by(By): By enum, ID, XPATH, etc.
            value:(str): pattern to find the element.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.
            visible:(bool): Flag to indicate if the element should visible or not
        
        Returns:
            str: Text from element.
        """
        if visible:
            return self.get_visible_element(by, value, driver, timeout).text
        return self.get_present_element(by, value, driver, timeout).text

    def switch_window(self, which_window:int=0) -> str:
        """
        Handle the switching windows

        Args:
            which_window(int:default=0): position of window to switch.

        Returns:
            str: current ulr from window.

        Raises:
            BrowserManagerException: unable to switch window
        """
        try:
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[which_window])
        except Exception as e:
            self.log.error(f"Unable to switch the current driver to window {which_window}")
            raise BrowserManagerException("Unable to switch window") from e
        return self.get_current_driver_url()
    
    def get_current_driver_url(self, driver=None) -> str:
        """
        Return url from given driver.

        Args:
            driver:(webdriver obj:Optional, Default=None): webdriver object.

        Returns:
            str: current url from give driver.
        """
        driver = driver or self.driver
        return driver.current_url

    def driver_down(self) -> None:
        """
        Teardown driver.
        """
        self.driver.quit()
