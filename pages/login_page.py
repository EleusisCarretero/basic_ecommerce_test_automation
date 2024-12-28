"""
Login page class
"""
from selenium.webdriver.common.by import By
from basic_ecommerce_test_automation.pages.base_pages import BasePage
from basic_ecommerce_test_automation.utils.tools import YamlManager



class LoginPage(BasePage):
    LOGIN_PAGE_DICT = {}
    def __init__(self, browser, testing_page):
        super().__init__(browser)
        self.LOGIN_PAGE_DICT = YamlManager.get_yaml_file_data(testing_page)["general_inputs"]["login_page"]
        self.testing_page = self.LOGIN_PAGE_DICT["path"]
        browser.open_page(self.testing_page)

    def get_valid_credentials(self):
        valid_credentials = []
        def get_credential(key, init=0, end=-1):
            by = self.LOGIN_PAGE_DICT[key]["by"]
            ele = self.LOGIN_PAGE_DICT[key]["element"]
            return self._convert_text_to_list(self.get_text_element(by, ele), "\n", init, end)
 
        users = get_credential("valid_users", 1)
        passwords = get_credential("valid_password", 1, 2)
        for user in users:
            valid_credentials.append({"user": user, "password": passwords[0]})
        return valid_credentials
    
    def write_credentials(self, user, password):
        def set_credentials(key, value):
            by = self.LOGIN_PAGE_DICT[key]["by"]
            ele = self.LOGIN_PAGE_DICT[key]["element"]
            self.set_element_value(by, ele, value)
        
        for key, value in {"username": user, "password": password}.items():
            set_credentials(key, value)

    def click_login_bttn(self):
        by = self.LOGIN_PAGE_DICT["login_bttn"]["by"]
        ele = self.LOGIN_PAGE_DICT["login_bttn"]["element"]
        self.click_on_element(by, ele)

    
    def login_page(self, user=None, password=None, credentials=True):
        # Write credentials if it is requested
        if credentials:
            self.write_credentials(user, password)
        # Click on login button
        self.click_login_bttn()

    def get_alert_text(self):
        return super().get_alert_text
    
    def acpet_alert(self):
        super().acpet_alert()
