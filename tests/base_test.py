"""
Contains the common base test classes and shared stuff
"""

from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager
from basic_ecommerce_test_automation.utils.tools import ApiManager, ApiManagerError


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
    
    def step_check_execution_events(self, callable_event, exceptions, *args, **kwargs):
        """
        Step function to validate the correct execution of an event like a click,
        a writing info, moving from one page to other, or even any other kind of callable event

        Args:
            callable_event(callable): method to execute
            exceptions(tuple): Exceptions to validate they have not been raised
            *args(list): arguments
            **kwargs(dict): arguments
        
        Returns:
            any: response from callable_event.
        """
        self.log.info(f"Evaluate the correct execution on {callable_event.__name__}")
        response = self.result.check_not_raises_any_given_exception(
            callable_event,
            exceptions,
            f"Check the {callable_event.__name__} event is secessfully executed using args {args} and kwargs {kwargs}",
            *args, **kwargs
        )
        assert self.result.step_status
        return response

    def step_execute_api_request(self, url, *args, **kwargs):
        """
        Step method to validate the correct execution of a api request

        Args:
            url(str): API's url
            *args(list): arguments
            **kwargs(dict): arguments

        Returns:
            any: response from callable_event.
        """

        self.log.info(f"Try response from url={url}")
        response = self.step_check_execution_events(
            ApiManager.get_api_response,
            ApiManagerError,
            url, *args, **kwargs
        )
        return response
