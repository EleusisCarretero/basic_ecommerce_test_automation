"""
General configuration
"""
import sys
import os
import subprocess
import time
import requests
import pytest
from utils.config import Config
from utils.logger_manager import LoggerManager
from utils.browser_manager import BrowserManager
from utils.result_manager import ResultManagerClass
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
        default="Edge",
        help="Browser to execute the tests"
    )


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


@pytest.fixture(scope="session")
def run_users_api(api_settings):
    """
    Fixture to get the instance of ResultManagerClass, common in all tests.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "utils/api.py")
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
            pytest.exit(" La API Flask no se inició correctamente.")
    except requests.ConnectionError:
        pytest.exit(" No se pudo conectar a la API Flask.")

    yield

    server.terminate()
    server.wait()
