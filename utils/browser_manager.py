"""
Browser manager class
"""
import os
import tempfile
from typing import Union
from enum import Enum
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager as FirefoxManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager as EdgeManager
from test_utils.logger_manager import LoggerManager


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
        return list(cls)


class ServiceManager(Enum):
    """Browser Services and manager"""
    CHROME = ChromeService, ChromeDriverManager
    FIREFOX = FirefoxService, FirefoxManager
    EDGE = EdgeService, EdgeManager


class SelectBy(Enum):
    """
    Enum class to handle the select methods
    """
    VISIBLE_TEXT = 1
    VALUE = 2
    INDEX = 3

    @classmethod
    def get_select_method_by(cls, select_by):
        """
        Classmethod to return the corresponding select method
        """
        return {
            cls.VISIBLE_TEXT: "select_by_visible_text",
            cls.VALUE: "select_by_value",
            cls.INDEX: "select_by_index",
        }.get(select_by, None)


class BrowserManagerException(Exception):
    """BrowserManager Exception class"""


class BrowserManager:
    """
    Class to manage with the webdriver instance.

    Attributes:
        log (logger): Logger instance.
        driver(Webdriver): Webdriver instance.
    """

    def __init__(self,
                 *args,
                 browser=AvailableBrowsers.CHROME,
                 url=None):
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self._driver = self._init_webdriver(browser, *args)
        if url:
            self.open_page(url)

    def _init_webdriver(self, browser, *args):
        """Initialize WebDriver"""
        if browser.capitalize() not in AvailableBrowsers.get_available_browsers():
            self.log.error(f"Browser {browser} is not available")
            raise BrowserManagerException(f"Browser {browser} is not available")

        options = getattr(webdriver, f"{browser}Options")()
        options.binary_location = "/usr/bin/google-chrome" 
        user_data_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--headless")
        for arg in args:
            options.add_argument(arg)

        try:
            service_class, manager = getattr(ServiceManager, browser.upper()).value
            driver_path = manager().install()

            # 🔴 Corregir detección de `chromedriver`
            chromedriver_executable = os.path.join(os.path.dirname(driver_path), "chromedriver")

            if not os.path.isfile(chromedriver_executable):
                self.log.error(f"❌ Chromedriver no encontrado en: {chromedriver_executable}")
                raise BrowserManagerException(f"Chromedriver no válido en {chromedriver_executable}")

            if not os.access(chromedriver_executable, os.X_OK):
                self.log.info(f"🔧 Asignando permisos de ejecución a {chromedriver_executable}")
            os.chmod(chromedriver_executable, 0o755)

            self.log.info(f"✅ Usando Chromedriver en: {chromedriver_executable}")

            service = service_class(chromedriver_executable)
            driver = getattr(webdriver, browser)(service=service, options=options)

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

    def open_page(self,
                  url:str,
                  driver=None) -> None:
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

    def get_webdriver_element_obj(self,
                                  driver,
                                  locator:tuple,):
        """
        Looks for an element, in driver, witch matches with the given by and value.

        Args:
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            locator(tuple): element locator.

        Returns:
            Element: element with matches the specifications.

        Raises:
            BrowserManagerException: In case there is no element in driver witch matches.
        """
        driver = driver or self.driver
        try:
            return driver.find_element(getattr(By, locator[0]), locator[1])
        except NoSuchElementException as e:
            self.log.error(f"Unable to find element with parameters ('{locator}')")
            raise BrowserManagerException("Unable to find element") from e

    def click_wait_clickable_element(self,
                                     locator:tuple,
                                     driver=None,
                                     timeout: Union[int, float]=10):
        """
        Waits until the element which matches with the 'by' and ' value' within
        a timeout and clicks on it, otherwise
        the BrowserManagerException is raised.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.

        Raises:
            BrowserManagerException: In case the timeout
            has been reached and the element is still not clickable.
        """
        driver = driver or self.driver
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((getattr(By, locator[0]), locator[1]))
            )
        except TimeoutException as e:
            self.log.error(f"Unable to have element '({locator})' clickable within {timeout}s")
            raise BrowserManagerException("Unable to get element clickable") from e
        element.click()

    def get_present_element(self,
                            locator:tuple,
                            driver,
                            timeout: Union[int, float]):
        """
        Waits until the element which matches with the 'by' and ' value'
        within a timeout, (it does not means it is visible) otherwise the
        BrowserManagerException is raised.

        Args:
            by(By): By enum, ID, XPATH, etc.
            locator(tuple): element locator.
            timeout: (int/float): Timeout in seconds to wait.

        Returns:
            Element: Element found which matches within timeout.

        Raises:
            BrowserManagerException: In case the timeout
            has been reached and the element is still not present.
        """
        driver = driver or self.driver
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((getattr(By, locator[0]), locator[1]))
            )
        except TimeoutException as e:
            self.log.error("Unable get the element using parameters "
                           f"'({locator})' within {timeout}s")
            raise BrowserManagerException("Unable to write on element") from e

    def get_present_list_element(self,
                                 locator:tuple,
                                 driver):
        """
        Waits until the element which matches with the 'by' and ' value'
        within a timeout, (it does not means it is visible)
        otherwise the BrowserManagerException is raised.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.

        Returns:
            Element: Element found which matches within timeout.

        Raises:
            BrowserManagerException: In case the timeout
            has been reached and the element is still not present.
        """
        driver = driver or self.driver
        try:
            return driver.find_elements(getattr(By, locator[0]), locator[1])
        except TimeoutException as e:
            self.log.error(f"Unable get the element using parameters '({locator})'")
            raise BrowserManagerException("Unable to write on element") from e

    def get_visible_element(self,
                            locator:tuple,
                            driver,
                            timeout: Union[int, float]):
        """
        Waits until the element which matches with the 'by' and ' value'
        within a timeout, (the element should be visible) otherwise the
        BrowserManagerException is raised.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.

        Returns:
            Element: Element found which matches within timeout.

        Raises:
            BrowserManagerException: In case the timeout has
            been reached and the element is still not visible.
        """
        driver = driver or self.driver
        try:
            return WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((getattr(By, locator[0]), locator[1]))
            )
        except TimeoutException as e:
            self.log.error("Unable get the element using parameters "
                           f"'({locator})' within {timeout}s")
            raise BrowserManagerException("Unable to get element") from e

    def enter_text_to_present_element(self,
                                      locator:tuple,
                                      keys_value:str,
                                      driver,
                                      timeout: Union[int, float]) -> None:
        """
        Writes a text ('keys_value') the located element, not necessary visible,
        with the 'by' and ' value' within a timeout, otherwise
        the BrowserManagerException is raised.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.
        """
        element = self.get_present_element(locator, driver, timeout)
        element.clear()
        element.send_keys(keys_value)

    def get_element_text(self,
                         locator:tuple,
                         driver,
                         timeout: Union[int, float],
                         visible=True) -> str:
        """
        Gets the text from an element.

        Args:
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
            timeout: (int/float): Timeout in seconds to wait.
            visible:(bool): Flag to indicate if the element should visible or not
        
        Returns:
            str: Text from element.
        """
        if visible:
            return self.get_visible_element(locator, driver, timeout).text
        return self.get_present_element(locator, driver, timeout).text

    def switch_window(self,
                      which_window:int=0) -> str:
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

    def get_current_driver_url(self,
                               driver=None) -> str:
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

    def select_dropdown_option(self,
                               method: SelectBy,
                               option_value,
                               locator:tuple,
                               driver=None):
        """
        Dropdown one element from web page based on the 'method' and 'option_value' to be found.

        Args:
            method(SelectBy): Selection method (e.g., "value", "index", "visible_text").
            option_value: Selection based on static method.
            locator(tuple): element locator.
            driver:(webdriver obj:Optional, Default=None): webdriver object.
        """
        driver = driver or self.driver
        try:
            dropdown = Select(driver.find_element(getattr(By, locator[0]), locator[1]))
            select_method = getattr(dropdown, SelectBy.get_select_method_by(method))
        except Exception as e:
            raise BrowserManagerException("Unable browser couldn't do the dropdown") from e
        return select_method(option_value)
