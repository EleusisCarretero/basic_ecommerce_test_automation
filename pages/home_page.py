"""
Home page class
"""
from basic_ecommerce_test_automation.pages.base_pages import BasePage
from basic_ecommerce_test_automation.utils.tools import YamlManager


class HomePageException(Exception):
    """HomePageError"""


class HomePage(BasePage):
      
    def __init__(self, browser, testing_page):
        super().__init__(browser)
        self.page_dict = YamlManager.get_yaml_file_data(testing_page)["general_inputs"]["inventory_page"]
        self.testing_page = self.page_dict["path"]

    def click_on_lateral_menu(self):
        self.click_on_element(
            *self._get_element_params(key="lateral_menu"))
    
    def get_lateral_menu_items(self):
        return self.get_webdriver_element_obj(*self._get_element_params(key="lateral_menu_items"))
    
    def click_on_log_out(self):
        all_menu_items = self.get_lateral_menu_items()
        self.click_on_element(*self._get_element_params(key="logout"), all_menu_items)

