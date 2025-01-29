"""
Contents the ResultManager Class and its corresponding exception
"""
from typing import Callable, Union
from .logger_manager import LoggerManager


class ResultManagerClassException(Exception):
    """ResultManagerClass Exception class"""


class ResultManagerClass:
    """
    This class handles assertions and logging of the results.

    Attributes:
        log (logger): Logger instance
        step_status(bool): Tracks the status of the last validation
    """
    def __init__(self):
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self._step_status = False

    @property
    def step_status(self) -> bool:
        """
        Returns the value of internal variable '_step_status'.
        """
        return self._step_status

    @step_status.setter
    def step_status(self, new_status):
        if new_status != self._step_status:
            self._step_status = new_status

    def _log_result(self, status: bool, step_msg: str, details: str = "") -> None:
        if status:
            self.log.info(f"PASSED - {step_msg}")
            self.step_status = True
        else:
            self.log.error(f"FAILED - {step_msg}")
            self.step_status = False
            if details:
                self.log.error(details)

    def check_equals_to(self, actual_value: any, expected_value: any, step_msg: str) -> None:
        """
        Validates that two values are equals and tracks the result.

        Args:
            actual_value(any): The result value gotten from a response.
            expected_value(any): The value to compare the results and ensure it is the expected.
            step_msg(str): Step message to give details of the assertion
        """
        try:
            assert actual_value == expected_value
            self._log_result(True, f"PASSED, Assert is Equals - {step_msg}")
        except AssertionError:
            details = f"Expected: '{expected_value}', but got: '{actual_value}'."
            if type(actual_value) != type(expected_value):
                details += f" Different types variables, actual_value type {type(actual_value)} != expected_value {type(expected_value)}"
            self._log_result(False, step_msg, details)

    def check_not_equals_to(self, actual_value: any, expected_value: any, step_msg: str) -> None:
        """
        Validates that two values are NOT equals and tracks the result.

        Args:
            actual_value(any): The result value gotten from a response.
            expected_value(any): The value to compare the results and ensure is NOT equals to.
            step_msg(str): Step message to give details of the assertion
        """
        try:
            assert actual_value != expected_value
            self._log_result(True, step_msg)
        except AssertionError:
            details = f"Expected NOT to be: '{expected_value}', but got: '{actual_value}'."
            self._log_result(False, step_msg, details)

    def check_not_raises_any_exception(self, method: Callable, step_msg: str, *args, **kwargs) -> None:
        """
        Validates that when a function/method is executed ANY type of exception is not raised.

        Args:
            method(func): The callback function to execute.
            step_msg(str): Step message to give details of the assertion
            args(list): arguments for 'method'.
            kwargs(dict): arguments for 'method'.
        """
        try:
            response = method(*args, **kwargs)
            self._log_result(True, step_msg)
            return response
        except Exception as e:
            details = f"The method '{method.__name__}' raised an exception: {e}."
            self._log_result(False, step_msg, details)
            self.step_status = False

    def check_not_raises_any_given_exception(self, method: Callable, exceptions: Union [Exception, tuple], step_msg: str, *args, **kwargs) -> None:
        """
        Validates that any of the 'given' exceptions is NOT raise, otherwise the validations fails.

        Args:
            method(func): The callback function to execute.
            exceptions (Exception): Exceptions, or tuple of exceptions to validate is/are NOT raised.
            step_msg(str): Step message to give details of the assertion.
            args(list): arguments for 'method'.
            kwargs(dict): arguments for 'method'.
        """
        if not isinstance(exceptions, tuple):
            exceptions = (exceptions,)
        try:
            response = method(*args, **kwargs)
            self._log_result(True, step_msg)
            return response
        except exceptions as e:
            details = f"The method '{method.__name__}' raised an exception: {e}."
            self._log_result(False, step_msg, details)
            self.step_status = False

    def check_less_equals(self, actual_value: Union[int:float], expected_less_equals: Union[int:float], step_msg: str):
        """
        Validates that two values are equals and tracks the result.

        Args:
            actual_value(any): The result value gotten from a response.
            expected_less_equals(any): The value to compare the results and ensure it is less or equals.
            step_msg(str): Step message to give details of the assertion
        """
        try:
            assert actual_value <= expected_less_equals
            self._log_result(True, step_msg)
        except AssertionError:
            details = f"Expected NOT to be: '{expected_less_equals}', but got: '{actual_value}'."
            self._log_result(False, step_msg, details)
