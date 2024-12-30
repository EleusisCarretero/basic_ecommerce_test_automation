"""
Contains all login test cases
"""
import pytest
from selenium.common.exceptions import ElementClickInterceptedException, InvalidElementStateException, NoSuchElementException
from basic_ecommerce_test_automation.pages.home_page import HomePage
from basic_ecommerce_test_automation.pages.login_page import LoginPage
from basic_ecommerce_test_automation.tests.base_test import BaseTest
from basic_ecommerce_test_automation.utils.tools import YamlManager


class BaseLogIn(BaseTest):
    TESTING_PAGE =  "E:/11)_Eleusis_Git_Stuf/basic_ecommerce_test_automation/tests/test_inputs/sauce_demo.yaml"
    def setup(self, browser, result):
        super().setup(browser, result)
        self.inventory_page_dict = YamlManager.get_yaml_file_data(self.TESTING_PAGE)["general_inputs"]["inventory_page"]
        self.login_page = LoginPage(
            browser,
            self.TESTING_PAGE
        )
        self.home_page = HomePage(
            browser,
            self.TESTING_PAGE
        )

    def step_check_login_successfully(self, user_credential:dict) -> None:
        """
        Step function to validate the correct login.

        Args:
            user_credential (dict): username: password, credentials to login.
        """
        step_msg = f"Check using credentials {user_credential} we are able to login successfully."
        self.result.check_not_raises_any_exception(
            self.login_page.login_page,
              step_msg,
              **user_credential
        )
        assert self.result.step_status


class TestPositiveFlows(BaseLogIn):
    """
    Test class to validate positive login flows
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, browser, result):
        super().setup(browser, result)
        self.login_page.open_page()

    def test_valid_login(self):
        """
        Check the valid users can access to page successfully.
        """
        # 1. Get the user credentials.
        user_credential = self.login_page.get_just_specific_user("standard_user")
        # 2. Check if we are able to login without exceptions.
        self.step_check_login_successfully(user_credential)
        # 3. Check the url correspond to the inventory url
        inventory_path = f"{self.login_page.testing_page}{self.inventory_page_dict['path']}"
        stp_msg = "Check the expected inventory path matches with the current url from opened window."
        self.result.check_equals_to(
            self.login_page.get_current_url(True),
            inventory_path,
            stp_msg
        )
        assert self.result.step_status

    def test_login_logout(self):
        """
        
        """
        # 1. Get the user credentials.
        user_credential = self.login_page.get_just_specific_user("standard_user")
        # 2. Check if we are able to login without exceptions.
        self.step_check_login_successfully(user_credential)
        #3. click on lateral menu
        self.result.check_not_raises_any_given_exception(
            method=self.home_page.click_on_lateral_menu,
            exceptions=(InvalidElementStateException, ElementClickInterceptedException, NoSuchElementException),
            step_msg=" Check lateral menu is clickable"
        )
        assert self.result.step_status
        # 4. Click on logout
        self.result.check_not_raises_any_given_exception(
            method=self.home_page.click_on_log_out,
            exceptions=(InvalidElementStateException, ElementClickInterceptedException, NoSuchElementException),
            step_msg="Check Logout successfully"
        )
        assert self.result.step_status
