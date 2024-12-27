from basic_ecommerce_test_automation.pages.base_pages import BasePage
from basic_ecommerce_test_automation.utils.tools import YamlManager
import pytest

class TestPositiveFlows(BasePage):

    def __init__(self):
        testing_page = YamlManager.get_yaml_file_data("basic_ecommerce_test_automation/tests/test_inputs/sauce_demo.yaml")
        super().__init__(testing_page)

    def test_valid_login(self):
        print(f"Content from source demo file: {self.testing_page}")