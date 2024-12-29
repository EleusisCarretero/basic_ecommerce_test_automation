"""
Contants all login test cases
"""
import pytest
from basic_ecommerce_test_automation.pages.login_page import LoginPage
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager
from basic_ecommerce_test_automation.utils.tools import YamlManager


class TestPositiveFlows:
    """
    Test class to validate positive login flows
    """
    TESTING_PAGE =  "E:/11)_Eleusis_Git_Stuf/basic_ecommerce_test_automation/tests/test_inputs/sauce_demo.yaml"

    @pytest.fixture(autouse=True)
    def setup(self, browser, result):
        self.inventory_page_dict = YamlManager.get_yaml_file_data(self.TESTING_PAGE)["general_inputs"]["inventory_page"]
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self.result = result
        self.login_page = LoginPage(
            browser,
            self.TESTING_PAGE
        )

    def test_valid_login(self):
        """
        Check the valid users can access to page successfully.
        """
        # 1. Get the user credentials.
        user_credential = self.login_page.get_just_specific_user("standard_user")
        # 2. Check if we are able to login without exceptions.
        step_msg = f"Check using credentials {user_credential} we are able to login successfully."
        self.result.check_not_raises_any_exception(
            self.login_page.login_page,
              step_msg,
              **user_credential
        )
        assert self.result.step_status
        # 3. Check the url correspond to the inventory url
        inventory_path = f"{self.login_page.testing_page}{self.inventory_page_dict['path']}"
        stp_msg = "Check the expected inventory path matches with the current url from opened window."
        self.result.check_equals_to(
            self.login_page.get_current_url(True),
            inventory_path,
            stp_msg
        )
        assert self.result.step_status
