from ui.base_web_element import BaseWebElement


class ErrorMessage(BaseWebElement):

    def __init__(self, driver, locator, name, timeout):
        super().__init__(driver, locator, name, timeout)
    
    def is_visible(self, tries:int=2):
        is_present = False
        while tries > 0:
            if super().is_visible():
                is_present = True
                break
            tries -=1
        return is_present
            
