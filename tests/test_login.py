from basic_ecommerce_test_automation.pages.login_page import LoginPage
import pytest

from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager




class TestPositiveFlows:


    @pytest.fixture(autouse=True)
    def setup(self):
        self.login_page = LoginPage("E:/11)_Eleusis_Git_Stuf/basic_ecommerce_test_automation/tests/test_inputs/sauce_demo.yaml")
        logger_manager = LoggerManager(active_logs=True, default_log_folder=self.__class__.__name__)
        self.log = logger_manager.get_logger(self.__class__.__name__)

    
    def test_valid_login(self):
        self.log.info(f"Content from source demo file: {self.login_page.testing_page}")