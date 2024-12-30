from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class BaseTest:

    def setup(self, browser, result):
        self.browser = browser
        self.result = result
        self.log = LoggerManager.get_logger(self.__class__.__name__)
