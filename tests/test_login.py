"""
Contains all login test cases
"""
import time
import pytest
from selenium.common.exceptions import \
(ElementClickInterceptedException,
 InvalidElementStateException,
 NoSuchElementException)
from pages.home_page import HomePage
from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.tools import YamlManager


class BaseLogIn(BaseTest):
    """
    Base class for login-related test cases.

    This class extends BaseTest and provides common attributes and functionality 
    shared among all login test classes.

    Attributes:
        browser: WebDriver instance used for browser automation.
        result: Stores the result of test steps and assertions.
        log: Logger instance for logging test events.
        inventory_page_dict (dict): Dictionary storing common input values 
            used across login test cases.
        login_page (LoginPage): Instance of the login page object.
        home_page (HomePage): Instance of the home page object.
        TESTING_PAGE (str): Path to the test configuration file.
    """
    browser = None
    result = None
    log = None
    inventory_page_dict = None
    login_page = None
    home_page = None
    TESTING_PAGE =  "tests/test_inputs/sauce_demo.yaml"

    def setup(self, browser, result):
        super().setup(browser, result)
        self.inventory_page_dict = YamlManager.get_yaml_file_data(
            self.TESTING_PAGE
        )["general_inputs"]["inventory_page"]
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

    def step_check_login_unsuccessfully(self,
                                        user_credential:dict,
                                        expected_error_msg,
                                        timeout=2) -> None:
        """
        Step function to validate incorrect login.

        Args:
            user_credential (dict): username: password, credentials to login.
        """
        # 1. correct login
        step_msg = f"Check using credentials {user_credential} we are able to login unsuccessfully."
        self.result.check_not_raises_any_exception(
            self.login_page.login_page,
              step_msg,
              **user_credential
        )
        assert self.result.step_status
        # 2. validate error message
        step_msg = "Check the error message is displayed as expected"
        current_error_msg = self.login_page.get_login_error_text(timeout=timeout)
        self.result.check_equals_to(
            actual_value=current_error_msg,
            expected_value=expected_error_msg,
            step_msg=step_msg
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

    @pytest.mark.Smoke
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
        stp_msg = \
            "Check the expected inventory path matches with the current url from opened window."
        self.result.check_equals_to(
            self.login_page.get_current_url(True),
            inventory_path,
            stp_msg
        )
        assert self.result.step_status

    def test_login_logout(self):
        """
        Validate the correct login and logout
        """
        # 1. Get the user credentials.
        user_credential = self.login_page.get_just_specific_user("standard_user")
        # 2. Check if we are able to login without exceptions.
        self.step_check_login_successfully(user_credential)
        #3. click on lateral menu
        self.result.check_not_raises_any_given_exception(
            method=self.home_page.click_on_lateral_menu,
            exceptions=(
                InvalidElementStateException,
                ElementClickInterceptedException,
                NoSuchElementException),
            step_msg=" Check lateral menu is clickable"
        )
        assert self.result.step_status
        # 4. Click on logout
        self.result.check_not_raises_any_given_exception(
            method=self.home_page.click_on_logout,
            exceptions=(
                InvalidElementStateException,
                ElementClickInterceptedException,
                NoSuchElementException),
            step_msg="Check Logout successfully"
        )
        assert self.result.step_status

    @pytest.mark.parametrize(
            ("timeout"), [(5), (10), (20)]
    )
    def test_login_timeout(self, timeout):
        """Test that login page takes the timeout to login"""
        self.log.info(f"Testing login page with a timeout of {timeout}s")
        # 1. Get the user credentials.
        user_credential = self.login_page.get_just_specific_user("standard_user")
        start_time = time.time()
        self.step_check_login_successfully(user_credential)
        end_time = time.time()
        # 2. Check time take is less that the timeout
        self.result.check_less_equals(
            end_time - start_time,
            timeout,
            f"Check the login page takes less equals to {timeout}s"
        )
        assert self.result.step_status


#TODO: move it to common resources file
ERROR_MSG = \
        "Epic sadface: Username and password do not match any user in this service"


class TestNegativeFlows(BaseLogIn):
    """
    Test class to validate negative flows.
    """
    @pytest.fixture(autouse=True)
    def setup(self, browser, result):
        super().setup(browser, result)
        self.login_page.open_page()

    @pytest.mark.parametrize(
            ("user", "password", "expected_error_mgs"),
            [
                ("Juan_Camaney", "12345",
                 ERROR_MSG),  # Invalid user, invalid password
                ("standard_user", "soy_123_wers",
                 ERROR_MSG),  # valid user, invalid password
                ("Uknowd_123_t", "secret_sauce",
                 ERROR_MSG)  # invalid user, 'valid' password
            ]
    )
    def test_invalid_credentials(self, user, password, expected_error_mgs):
        """
        Validate invalid credentials

        Args:
            user(str): user credential.
            password(str): password credentials.
            expected_error_mgs(str): expected error message shown when a wrong user tries to login.
        """
        self.step_check_login_unsuccessfully(
            user_credential={"user":user,"password":password},
            expected_error_msg=expected_error_mgs
        )

    @pytest.mark.parametrize(
            ("user", "password", "expected_error_msg"),
            [
                ("standard_user", "", "Epic sadface: Password is required"),  # Empty password
                ("", "secret_sauce", "Epic sadface: Username is required"),  # Empty user
                ("", "", "Epic sadface: Username is required")  # Empty user and empty password
            ]
    )
    def test_empty_credentials(self, user, password, expected_error_msg):
        """
        Validate empty credentials, user, password or both.

        Args:
            user(str): user credential.
            password(str): password credentials.
            expected_error_mgs(str): expected error message shown when a wrong user tries to login.
        """
        self.step_check_login_unsuccessfully(
            user_credential={"user":user,"password":password},
            expected_error_msg=expected_error_msg
        )
