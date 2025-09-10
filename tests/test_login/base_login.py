from pages.login_page import LoginPage
from tests.base_test import BaseTest
from pages.home_page import HomePage
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
            self.login_page.logining,
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
            self.login_page.logining,
              step_msg,
              **user_credential  
        )
        assert self.result.step_status
        # 2. validate error message
        step_msg = "Check the error message is displayed as expected"
        is_visible = self.login_page.error_message(error_msg=expected_error_msg,timeout=timeout).is_visible()
        self.result.check_equals_to(
            actual_value=is_visible,
            expected_value=True,
            step_msg=step_msg
        )
        assert self.result.step_status