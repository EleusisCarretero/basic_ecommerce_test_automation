"""
General configuration
"""
import sys
import os
import subprocess
import tempfile
import time
import requests
import pytest
from test_utils.config import Config
from test_utils.logger_manager import LoggerManager
from test_utils.result_manager import ResultManagerClass
from utils.browser_manager import BrowserManager, BrowserOptions
from contextlib import contextmanager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def pytest_addoption(parser):
    """
    Defines the costume console inputs to run the tests
    """
    parser.addoption(
        "--log_folder",
        action="store",
        default="Logs",
        help="Folder to store logs"
    )
    parser.addoption(
        "--browser_type",
        action="store",
        default="Chrome",
        help="Browser to execute the tests"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default="",
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--start-maximized",
        action="store_true",
        default="",
        help="Set window maximized"
    )
    parser.addoption(
        "--disable-gpu",
        action="store_true",
        default="",
        help="Disable GPU"
    )
    parser.addoption(
        "--no-sandbox",
        action="store_true",
        default="",
        help="Disable sandbox"
    )
    parser.addoption(
        "--disable-dev-shm-usage",
        action="store_true",
        default="",
        help="Disable shared memory usage"
    )


@pytest.fixture(scope="session", autouse=True)
def configure_logging(pytestconfig):
    """
    Fixture that setups the common logger.
    """
    log_folder = pytestconfig.getoption("log_folder")
    if not log_folder:
        raise Exception(f"Variable empty {log_folder}")
    Config.log_folder = "logs_folder"
    LoggerManager.setup_logger()


@pytest.fixture(scope="class")
def browser(pytestconfig):
    """
    Fixture to setup the instance for BrowserManager common in all test cases.
    """
    browser_options = []
    browser_type =  pytestconfig.getoption("browser_type")

    for input_browser in BrowserOptions:
        if pytestconfig.getoption(input_browser.value):
            browser_options.append(input_browser.value)

    manager = BrowserManager(*browser_options, browser=browser_type)
    yield manager
    manager.driver_down()


@pytest.fixture(scope="class")
def result():
    """
    Fixture to get the instance of ResultManagerClass, common in all tests.
    """
    return ResultManagerClass()


@pytest.fixture(scope="session")
def run_users_api(api_settings):
    """
    Fixture to get the instance of ResultManagerClass, common in all tests.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "utils/api.py")
    with start_server(file_path, api_settings):
        response = requests.get("http://127.0.0.1:5000", timeout=10)
        assert response.status_code == 200

@contextmanager
def start_server(file_path: str, api_settings: str):
    """
    Start API server

    Args:
        file_path(str): path to api.py file
        api_settings(str): mongo configurations
    """
    server = subprocess.Popen(
        [
            "python",
            file_path,
            "--mongo_uri",
            api_settings["mongo_uri"],
            "--db_name",
            api_settings["db_name"],
            "--collection_name",
            api_settings["collection_name"]
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        shell=True
    )

    time.sleep(3)

    try:
        response = requests.get("http://127.0.0.1:5000", timeout=10)
        if response.status_code != 200:
            pytest.exit("API didn't initialize")
    except requests.ConnectionError:
        pytest.exit("Unable to connect to the API")

    try:
        yield
    finally:
        server.terminate()
        server.wait()
