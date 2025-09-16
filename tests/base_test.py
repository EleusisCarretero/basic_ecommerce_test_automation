"""
Contains the common base test classes and shared stuff
"""
from typing import List
from ui.base_web_element import BaseWebElementException
from ui.button import Button
from ui.input import Input
from utils.tools import ApiManager, ApiManagerError
from utils.browser_manager import BrowserManagerException
from test_utils.logger_manager import LoggerManager


class BaseTest:
    """
    Common base test class, shares the common setup, teardown, and step methods shared for all the
    test classes of the different features.

    Attributes:
        browser(BrowserManager): Instance of the browser manager to handle WebDriver.
        result(ResultManager): Instance of the result manager to handle all
                               the assertions and validations
        log (logger): Logger instance
    """
    browser = None
    result = None
    log = None


    def setup(self, browser, result):
        """
        Setup the common attributes for all the test classes
        """
        self.browser = browser
        self.result = result
        self.log = LoggerManager.get_logger(self.__class__.__name__)
    
    def check_input_fill(self, input_element: Input, value:str):
        self.log.info(f"Check the input element {input_element.name} has the expected value")
        self.result.check_equals_to(
            actual_value=input_element.text,
            expected_value=value,
            step_msg=f"The input element {input_element.name} has the correct value {value}"
        )
        assert self.result.step_status
    
    def check_simple_click(self, button_element: Button):
        self.log.info(f"Check the button element {button_element.name} has perform simple click successfully")
        self.result.check_not_raises_any_given_exception(
        button_element.click,
        BaseWebElementException,
        f"Check the button element {button_element.name} has perform simple click successfully"
        )
        assert self.result.step_status
    
    def check_url_after_event(self, event_callback, is_equals=True):
        current_url = self.browser.get_current_driver_url()
        if is_equals:
            self.log.info(f"Check the url from current page is equals to the expected  {expected_url}")
            self.result.check_equals_to(
            actual_value=current_url,
            expected_value=expected_url,
            step_msg=f"Check new page url {current_url} matches with the expected {expected_url}"
            )
        else:
            self.log.info(f"Check the url from current page is NOT equals to the expected  {expected_url}")
            self.result.check_not_equals_to(
            actual_value=current_url,
            expected_value=expected_url,
            step_msg=f"Check new page url {current_url} NOT matches with the expected {expected_url}"
            )

    def step_check_fill_and_click(self, input_elements:dict, button_element: Button, url_changed=False):
        current_url = ""
        self.log.info("Check all the input elements are correctly filled and clicking successfully")
        for input_element in input_elements:
            self.check_input_fill(**input_element)
        if url_changed:
            self.check_simple_click(button_element=button_element)
        

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
            f"Check the {callable_event.__name__} event is secessfully "
            f"executed using args {args} and kwargs {kwargs}",
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

    def step_move_to_next_page(self, change_page_method, page_obj):
        """
        Step function to validate the movement from cart page to checkout page
        """
        self.result.check_not_raises_any_given_exception(
            method=change_page_method,
            exceptions=BrowserManagerException,
            step_msg="Check the it is successfully move the desired page"
        )
        assert self.result.step_status
        # validate the current url vs the expected
        expected_url = page_obj.testing_page
        current_url = page_obj.get_current_url().split("/")[-1]
        self.result.check_equals_to(
            actual_value=current_url,
            expected_value=expected_url,
            step_msg=f"Check new page url {current_url} matches with the expected {expected_url}"
        )
        assert self.result.step_status
