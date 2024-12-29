"""
General configuration
"""
import pytest
from basic_ecommerce_test_automation.utils.config import Config
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager
from basic_ecommerce_test_automation.utils.browser_manager import BrowserManager
from basic_ecommerce_test_automation.utils.result_manager import ResultManagerClass


def pytest_addoption(parser):
    parser.addoption("--log_folder", action="store", default="Logs", help="Folder to store logs")

@pytest.fixture(scope="session", autouse=True)
def configure_logging(pytestconfig):
    """
    """
    log_folder = pytestconfig.getoption("log_folder")
    Config.log_folder = log_folder
    LoggerManager.setup_logger()


@pytest.fixture(scope="class", params=["Edge"])
def browser(request):
    manager = BrowserManager(browser=request.param)
    yield manager
    manager.driver_down()


@pytest.fixture(scope="class")
def result():
    return ResultManagerClass()