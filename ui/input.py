
from ui.base_web_element import BaseWebElement, Element

class InputException(Exception):
    pass


class Input(BaseWebElement):

    def __init__(self, driver, locator, name, timeout):
        super().__init__(driver, locator, name, timeout)
    
    def write(self, input_text, clean=True) -> None:
        if(not self.is_visible()):
            raise InputException("The input element is not visible")
        if(clean):
            self.element.clear()
        self.element.send_keys(input_text)