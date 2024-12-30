"""
Base test page class
"""
from selenium.webdriver.common.by import By
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class BasePageException(Exception):
    """Exception for BasePage class"""
    pass

class BasePage:

    page_dict = {}

    def __init__(self, browser):
        self.driver = browser.get_driver()
        self.browser = browser
        self.log = LoggerManager.get_logger(self.__class__.__name__)

    @property
    def testing_page(self):
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
    
    def _get_webdriver_element_obj(self, by, value, driver=None, timeout=5):
        driver = driver or self.browser.driver
        return self.browser.get_web_element(by=by, value=value, driver=driver, timeout=timeout)
        
    def click_on_element(self, by, value, driver=None):
        driver = driver or self.browser.driver
        self.browser.click_located_element(by=by, value=value, driver=driver)
    
    def get_text_element(self, by, value, driver=None):
        driver = driver or self.browser.driver
        return self.browser.get_text_from_element(by=by, value=value, driver=driver)

    def set_element_value(self, by, value, keys_value, driver=None):
        driver = driver or self.browser.driver
        self.browser.enter_text_to_element(by=by, value=value, driver=driver, keys_value=keys_value)
        
    def get_alert_text(self):
        try:
            alert = self.driver.switch_to.alert
        except AttributeError as e:
            self.log.error("No such attribute")
            raise BasePageException("Element not having text") from e
        self.driver.active_element()
        return alert.text
    
    def acpet_alert(self):
        try:
            alert = self.driver.switch_to.alert
        except AttributeError as e:
            self.log.error("No such attribute")
            raise BasePageException("Element not having text") from e
        alert.acept()

    def get_current_url(self, switch=False):
        if switch:
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[0])
        return self.driver.current_url


    
    @staticmethod
    def _convert_text_to_list(text, spliter, ini=0, end=-1):
        return text.split(spliter)[ini:end]

