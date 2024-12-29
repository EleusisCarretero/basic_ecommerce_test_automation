from basic_ecommerce_test_automation.utils.logger_manager import LoggerManager


class ResultManagerClass:
    def __init__(self):
        self.log = LoggerManager.get_logger(self.__class__.__name__)
        self._step_status = False

    @property
    def step_status(self):
        return self._step_status
    
    @step_status.setter
    def step_status(self, new_status):
        if new_status != self._step_status:
            self._step_status = new_status

    def check_equals_to(self, actual_value, expected_value, step_msg):
        try:
            assert actual_value == expected_value
            self.log.info(f"PASSED, Assert Equals - {step_msg}")
            self.step_status = True
        except AssertionError as e:
            self.log.error(f"FAILED, Assert NOT Equals - {step_msg}")
            self.log.error(f"The given actual value: '{actual_value}' IS NOT EQUAL TO the expected value: {expected_value}")
            self.step_status = False

    def check_not_equals_to(self, actual_value, expected_value, step_msg):
        try:
            assert actual_value != expected_value
            self.log.info(f"PASSED, Assert NOT Equals - {step_msg}")
        except AssertionError as e:
            self.log.error(f"FAILED, Assert Equals - {step_msg}")
            self.log.error(f"The given actual value: '{actual_value}' IS EQUAL TO the expected value: {expected_value}")

    def check_not_raises_any_exception(self, method, step_msg, *args, **kwars):
        try:
            response = method(*args, **kwars)
            self.log.info(f"PASSED, Assert NOT raises exception - {step_msg}")
            self.step_status = True
            return response
        except Exception as e:
            self.log.error(f"FAILED, Assert Raises excpetion - {step_msg}")
            self.log.error(f"The given method: '{method.__name__}' HAS RAISED the exception {e}")
            self.step_status = False