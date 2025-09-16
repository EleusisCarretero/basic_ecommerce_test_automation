
from ui.base_web_element import BaseWebElement, BaseWebElementException
from selenium.webdriver.support import expected_conditions as EC


class ButtonException(Exception):
    pass


class Button(BaseWebElement):
    
    def __init__(self, driver, locator, name, timeout):
        super().__init__(driver, locator, name, timeout)

    
    def _common_click(self):
        self.move_on(EC.element_to_be_clickable(self._element.locator()))

    def click(self):
        try:
            self._common_click()
            self.actions.click(self.element).perform()
        except BaseWebElementException as e:
            self.log.error(f"Not clicked because exception: {e}")
            raise ButtonException("No click on button element") from e