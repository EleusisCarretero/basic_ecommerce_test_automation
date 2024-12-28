"""
Base test page class
"""
from selenium.webdriver.common.by import By
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class BasePageException(Exception):
    """Exception for BasePage class"""
    pass

class BasePage:

    def __init__(self, browser):
        self.driver = browser.get_driver()
        self.log = LoggerManager.get_logger(self.__class__.__name__)

    def get_text_element(self, by, element):
        try:
            text_element = self.driver.find_element(getattr(By, by), element).text
        except AttributeError as e:
            self.log.error("No such attribute")
            raise BasePageException("Element not having text") from e
        return text_element

    def set_element_value(self, by, element, value):
        try:
            self.driver.find_element(getattr(By, by), element).send_keys(value)
        except AttributeError as e:
            self.log.error("No such attribute")
            raise BasePageException("Element not having text") from e
        
    def click_on_element(self, by, element):
        try:
            self.driver.find_element(getattr(By, by), element).click()
        except AttributeError as e:
            self.log.error("No such attribute")
            raise BasePageException("Element not having text") from e
        
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

    
    @staticmethod
    def _convert_text_to_list(text, spliter, ini=0, end=-1):
        return text.split(spliter)[ini:end]


    @property
    def testing_page(self):
        return self._testing_page
    
    @testing_page.setter
    def testing_page(self, new_value):
        self._testing_page = new_value
