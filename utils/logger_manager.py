import os
import logging
from datetime import datetime
from pathlib import Path
import subprocess


class LoggerManager:
    LOG_COUNTER = 0
    def __init__(self, active_logs=True, default_log_folder="DEFAULT_LOG_FOLDER"):
        self.active_logs = active_logs
        self._setup_logger(default_log_folder)
    
    def count_files_with_extension(self, folder_path, extension=".log"):
        if not extension.startswith("."):
            extension = f".{extension}"
        
        # Contar archivos con la extensión dada
        count = sum(1 for file in os.listdir(folder_path) if file.endswith(extension))
        return count

    def _setup_logger(self, default_log_folder):
        current_file_path  = os.path.abspath(__file__)
        caller_file_name = current_file_path.split("\\")[-1].strip(".py")
        current_dir = self._get_repo_path()
        default_log_folder_path = os.path.join(current_dir, "test_logs_results",default_log_folder)
        try:
            os.makedirs(default_log_folder_path)
        except FileExistsError:
            print("Folder already exists")
        
        self.LOG_COUNTER = self.count_files_with_extension(default_log_folder_path)

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        if self.active_logs:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # Configurar file handler
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
            file_handler = logging.FileHandler(
                f"{os.path.join(default_log_folder_path, caller_file_name)}_{formatted_datetime}_{self.LOG_COUNTER}.log"
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    @staticmethod
    def _get_repo_path():
        """
        """
        repo_path = None
        current_path = Path(__file__).resolve()
        for parent in current_path.parents:
            if (parent / "README.md").exists():
                repo_path = parent
                break
        return repo_path


    def get_logger(self, name):
        return logging.getLogger(name)

if __name__ == '__main__':
    # test the logger
    local_logger = LoggerManager(active_logs=True).get_logger("mylogger")
    local_logger.info("Save info")
    local_logger.error("Showing error")