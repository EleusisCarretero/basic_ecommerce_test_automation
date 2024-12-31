"""
General configuration
"""
import pytest
from basic_ecommerce_test_automation.utils.config import Config
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager
from basic_ecommerce_test_automation.utils.browser_manager import BrowserManager
from basic_ecommerce_test_automation.utils.result_manager import ResultManagerClass


def pytest_addoption(parser):
    """
    Defines the costume console inputs to run the tests
    """
    parser.addoption("--log_folder", action="store", default="Logs", help="Folder to store logs")
    parser.addoption("--browser_type", action="store", default="Edge", help="Browser to execute the tests")


@pytest.fixture(scope="session", autouse=True)
def configure_logging(pytestconfig):
    """
    Fixture that setups the common logger.
    """
    log_folder = pytestconfig.getoption("log_folder")
    Config.log_folder = log_folder
    LoggerManager.setup_logger()


@pytest.fixture(scope="class")
def browser(pytestconfig):
    """
    Fixture to setup the instance for BrowserManager common in all test cases.
    """
    browser_type =  pytestconfig.getoption("browser_type")
    manager = BrowserManager(browser=browser_type)
    yield manager
    manager.driver_down()


@pytest.fixture(scope="class")
def result():
    """
    Fixture to get the instance of ResultManagerClass, common in all tests.
    """
    return ResultManagerClass()
