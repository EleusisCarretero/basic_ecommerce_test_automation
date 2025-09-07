
from ui.base_web_element import BaseWebElement
from selenium.webdriver.support import expected_conditions as EC


class Button(BaseWebElement):
    
    def __init__(self, driver, locator, name, timeout):
        super().__init__(driver, locator, name, timeout)

    
    def _common_click(self):
        self.move_on(EC.element_to_be_clickable(self._element.locator()))


    def click(self):

        self._common_click()
        self.actions.click(self.element).perform()