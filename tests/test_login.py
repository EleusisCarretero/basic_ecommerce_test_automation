import pytest
from basic_ecommerce_test_automation.pages.login_page import LoginPage
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class TestPositiveFlows:

    @pytest.fixture(autouse=True)
    def setup(self, browser):
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self.login_page = LoginPage(
            browser,
            "E:/11)_Eleusis_Git_Stuf/basic_ecommerce_test_automation/tests/test_inputs/sauce_demo.yaml")

    def test_valid_login(self):
        self.log.info(f"Content from source demo file: {self.login_page.testing_page}")