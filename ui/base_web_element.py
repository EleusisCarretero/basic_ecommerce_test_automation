"""
Base Web Element file class
"""
from test_utils.logger_manager import LoggerManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from dataclasses import dataclass



@dataclass
class Element:
    by: str
    path: str
    driver: webdriver

    def locator(self) -> tuple:
        return getattr(By, self.by), self.path

    def element(self):
        return self.driver.find_element(*self.locator())



class BaseWebElementException(Exception):
    pass


class BaseWebElement:
    TIMEOUT = 45

    def __init__(self, driver, locator, name, timeout):
        self._driver = driver
        self._element = Element(*locator, driver)
        self._locator = locator
        self._name = name
        self.timeout = timeout or self.TIMEOUT
        self.wait = WebDriverWait(driver, timeout)
        self.actions = ActionChains(driver)
        self.log = LoggerManager.get_logger(self.__class__.__name__)
    
    @property
    def driver(self):
        return self._driver

    @property
    def element(self):
        return self._element.element()
    
    @property
    def name(self):
        return self._name
    
    @property
    def locator(self):
        by, path = self._locator
        return getattr(By, by), path
    
    @locator.setter
    def locator(self, new_locator):
        if isinstance(new_locator, tuple):
            self._locator = new_locator
        elif isinstance(new_locator, By):
            self._locator[0] = new_locator
        else:
            self._locator[1] = new_locator
        

    def is_visible(self):
        """
        Waits until the element which matches with the 'by' and ' value'
        within a timeout, (the element should be visible) otherwise the
        BrowserManagerException is raised.

        Returns:
            Boolean: Returns if the element is visible within timeout.

        Raises:
            BrowserManagerException: In case the timeout has
            been reached and the element is still not visible.
        """
        is_visible = False
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.locator)
            )
            is_visible = True
        except TimeoutException as e:
            self.log.error("Element is not visible on "
                           f"'({self.locator})' within {self.timeout}s: {e}")
        except Exception as e:
            self.log.error(f"Unknow excpetion: {e}")
        return is_visible

    def get_text(self) -> str:
        return self.element.get_attribute("value")
    
    def move_on(self, *extra_expected_conditions) -> None:
        try:
            self.wait.until(
                EC.all_of(
                    EC.presence_of_element_located(self._element.locator()),
                    EC.visibility_of_element_located(self._element.locator()),
                    *extra_expected_conditions
                )
            )
            self.actions.move_to_element(self.element).perform()
        except TimeoutException as e:
            self.log.error("Element is not visible on "
                           f"'({self._element.locator()})' within {self.timeout}s: {e}")
            raise BaseWebElementException("Unable to move on element") from e