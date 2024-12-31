"""
Contains the common base test classes and shared stuff
"""

from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class BaseTest:
    """
    Common base test class, shares the common setup, teardown, and step methods shared for all the
    test classes of the different features.

    Attributes:
        browser(BrowserManager): Instance of the browser manager to handle WebDriver.
        result(ResultManager): Instance of the result manager to handle all the assertions and validations
        log (logger): Logger instance
    """

    def setup(self, browser, result):
        """
        Setup the common attributes for all the test classes
        """
        self.browser = browser
        self.result = result
        self.log = LoggerManager.get_logger(self.__class__.__name__)
