"""
Login page class
"""
from pages.base_pages import BasePage
from ui.error_message import ErrorMessage
from ui.input import Input
from ui.button import Button
from utils.tools import YamlManager


class LoginPageException(Exception):
    """
    LoginPase error
    """


class LoginPage(BasePage):
    """
    Class to manage all the functionalities related to the login page.

    Attributes:
        LOGIN_PAGE_DICT (dict): Saves al the needed and/or relevant inputs for login page
        testing_page (str): Login page path
    """
    TIMEOUT = 60
    def __init__(self,
                 browser,
                 testing_page):
        super().__init__(browser)
        self.page_dict = YamlManager.get_yaml_file_data(
            testing_page
        )["general_inputs"]["login_page"]
        self.testing_page = self.page_dict["path"]
        self._user_name = Input(driver=browser.driver, locator=self._get_element_params("username"), name="username_input", timeout=60)
        self._password = Input(driver=browser.driver, locator=self._get_element_params("password"), name="password_input", timeout=60)
        self._login_button = Button(driver=browser.driver, locator=self._get_element_params("login_bttn"), name="login_button", timeout=60)

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    @property
    def login_button(self):
        return self._login_button

    def _login(self, user_name=None, password=None):
        if user_name:
            self.user_name.write(user_name)
        if password:
            self.password.write(password)
        self.login_button.click()
    
    
    def logining(self,
                 user_name=None,
                 password=None):
        """
        Tries to logins.

        With the given 'user' and 'password' or not it tries to logins.

        Args:
            user (str:optional): User name
            password (str:optional): corresponding password
            credentials (bool:optional:default=True): Flag to try to login with or without
        """
        self.log.info("Tying to login")
        self.log.debug(f"{user_name=}, {password=}")
        # Write credentials if it is requested
        self._login(user_name=user_name, password=password)
    
    def get_valid_credentials(self):
        """
        Gives back a list with all the available user credentials from https://www.saucedemo.com/

        It uses the internal method get_credential to specifically read
        the users from "Accepted usernames are", and the uniq valid password
        for all of them from  "Password for all users".

        Returns:
            List: Dictionaries with valid user and its corresponding password.
        
        Example:
            >>> get_valid_credentials()
            [{'user': 'standard_user', 'password': 'secret_sauce'}, ....]
        """
        valid_credentials = []
        def get_credential(key, init=0, end=-1):
            """
            Gets the 'By' method and the webdriver element to look for the user credetials and
            returns the text values in list format
            """
            return self._convert_text_to_list(
                self.get_text_element(self._get_element_params(key)), "\n", init, end)

        users = get_credential("valid_users", 1)
        passwords = get_credential("valid_password", 1, 2)
        for user in users:
            valid_credentials.append({"user_name": user, "password": passwords[0]})
        return valid_credentials

    def get_just_specific_user(self,
                               desired_user: str):
        """
        Returns the specific credentials for the 'desired' user.

        Args:
            desired_user (str): user name
        
        Returns:
            dict: user name with its password.
        
        Raises:
            LoginPageException: if the user is not part of the valid users
        """
        users = self.get_valid_credentials()
        for user in users:
            if user["user_name"] == desired_user:
                return user
        self.log.error(f"{desired_user} is not part of the valid users form {users}. "
                       f"Check the 'accepted' users from {self.testing_page }")
        raise LoginPageException(f"{desired_user} is not a valid user")

    def error_message(self, error_msg: str, timeout=None):
        """
        Returns the text from error message.

        Returns:
            str: text from error message displayed after a wrong login.
        """
        by, value = self._get_element_params("wrong_credential_error")
        timeout = timeout or self.TIMEOUT
        return super().error_message(
            locator=(by, value.format(error_msg=error_msg)),
            name="Login page error message",
            timeout=timeout)