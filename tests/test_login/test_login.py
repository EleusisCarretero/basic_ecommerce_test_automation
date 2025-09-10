"""
Contains all login test cases
"""
import time
import pytest
from selenium.common.exceptions import \
(ElementClickInterceptedException,
 InvalidElementStateException,
 NoSuchElementException)
from tests.test_login.base_login import BaseLogIn


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
            ("user_name", "password", "expected_error_mgs"),
            [
                ("Juan_Camaney", "12345",
                 ERROR_MSG),  # Invalid user, invalid password
                ("standard_user", "soy_123_wers",
                 ERROR_MSG),  # valid user, invalid password
                ("Uknowd_123_t", "secret_sauce",
                 ERROR_MSG)  # invalid user, 'valid' password
            ]
    )
    def test_invalid_credentials(self, user_name, password, expected_error_mgs):
        """
        Validate invalid credentials

        Args:
            user_name(str): user credential.
            password(str): password credentials.
            expected_error_mgs(str): expected error message shown when a wrong user tries to login.
        """
        self.step_check_login_unsuccessfully(
            user_credential={"user_name":user_name,"password":password},
            expected_error_msg=expected_error_mgs
        )

    @pytest.mark.parametrize(
            ("user_name", "password", "expected_error_msg"),
            [
                ("standard_user", "", "Epic sadface: Password is required"),  # Empty password
                ("", "secret_sauce", "Epic sadface: Username is required"),  # Empty user
                ("", "", "Epic sadface: Username is required")  # Empty user and empty password
            ]
    )
    def test_empty_credentials(self, user_name, password, expected_error_msg):
        """
        Validate empty credentials, user, password or both.

        Args:
            user_name(str): user credential.
            password(str): password credentials.
            expected_error_mgs(str): expected error message shown when a wrong user tries to login.
        """
        self.step_check_login_unsuccessfully(
            user_credential={"user_name":user_name,"password":password},
            expected_error_msg=expected_error_msg
        )
