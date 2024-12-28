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
        users = self.login_page.get_valid_credentials()
        self.log.info(f"Accepted users: {users}")
        user = users[0]
        self.login_page.login_page(user["user"], user["password"])
        alert_text = self.login_page.get_alert_text()
        self.log.info(f"Alert Text: {alert_text}")
        self.login_page.acpet_alert()