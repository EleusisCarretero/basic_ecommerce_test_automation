"""
General configuration
"""
import pytest
from basic_ecommerce_test_automation.utils.browser_manager import BrowserManager
from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager
# from utils.logger_manager import LoggerManager, BrowserManager

def pytest_addoption(parser):
    parser.addoption("--log_folder", action="store", default="Logs", help="Folder to store logs")

@pytest.fixture(scope="session")
def folder(pytestconfig):
    return pytestconfig.getoption("log_folder")



@pytest.fixture(scope="session")
def logger(folder):
    logger_manager = LoggerManager(active_logs=True, default_log_folder=folder)
    return logger_manager

@pytest.fixture(scope="class", params=["Edge"])
def browser(request, logger):
    manager = BrowserManager(logger, browser=request.param)
    yield manager
    manager.driver_down()