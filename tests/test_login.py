from basic_ecommerce_test_automation.pages.login_page import LoginPage
import pytest




class TestPositiveFlows:


    @pytest.fixture(autouse=True)
    def setup(self):
        self.login_page = LoginPage("E:/11)_Eleusis_Git_Stuf/basic_ecommerce_test_automation/tests/test_inputs/sauce_demo.yaml")

    
    def test_valid_login(self):
        print(f"Content from source demo file: {self.login_page.testing_page}")