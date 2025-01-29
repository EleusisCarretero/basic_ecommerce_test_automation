"""
Contains logger manager class
"""
import os
import logging
from datetime import datetime
from pathlib import Path
from .config import Config


class LoggerManager:
    """"
    Class logger manager is responsible of setting the logger setup and handle all the logger used in the repo.

    Attributes:
        LOG_COUNTER(int): saves the current log value created in the run.
        _loggers(dict): internal dictionary to manage all the loggers created and assigned.
    """
    LOG_COUNTER = 0
    _loggers = {}

    @classmethod
    def get_logger(cls, name:str):
        if name in LoggerManager._loggers:
            return LoggerManager._loggers[name]
        LoggerManager._loggers[name] = logging.getLogger(name)
        return LoggerManager._loggers[name]

    @classmethod
    def setup_logger(cls):
        """
        Method to setup the logger. Creates the test folder to save the logs and controls the name
        and enumeration of the log file. As well as setup the format and level.
        """
        current_file_path  = os.path.abspath(__file__)
        caller_file_name = current_file_path.split("\\")[-1].strip(".py")
        current_dir = cls._get_repo_path()
        log_folder = Config.log_folder
        default_log_folder_path = os.path.join(current_dir, log_folder)
        try:
            os.makedirs(default_log_folder_path)
        except FileExistsError:
            print("Folder already exists")

        cls.LOG_COUNTER = cls._count_files_with_extension(default_log_folder_path)

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
        file_handler = logging.FileHandler(
            f"{os.path.join(default_log_folder_path, caller_file_name)}_{formatted_datetime}_{cls.LOG_COUNTER}.log"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    @staticmethod
    def _count_files_with_extension(folder_path, extension=".log"):
        if not extension.startswith("."):
            extension = f".{extension}"
        count = sum(1 for file in os.listdir(folder_path) if file.endswith(extension))
        return count

    @staticmethod
    def _get_repo_path():
        repo_path = None
        current_path = Path(__file__).resolve()
        for parent in current_path.parents:
            if (parent / "README.md").exists():
                repo_path = parent
                break
        return repo_path

if __name__ == '__main__':
    # test the logger
    local_logger = LoggerManager(active_logs=True).get_logger("mylogger")
    local_logger.info("Save info")
    local_logger.error("Showing error")
