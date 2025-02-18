"""
Login page class
"""
from pages.base_pages import BasePage
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
    def __init__(self,
                 browser,
                 testing_page):
        super().__init__(browser)
        self.page_dict = YamlManager.get_yaml_file_data(
            testing_page
        )["general_inputs"]["login_page"]
        self.testing_page = self.page_dict["path"]

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
            return self._convert_text_to_list(self.get_text_element(self._get_element_params(key)), "\n", init, end)

        users = get_credential("valid_users", 1)
        passwords = get_credential("valid_password", 1, 2)
        for user in users:
            valid_credentials.append({"user": user, "password": passwords[0]})
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
            if user["user"] == desired_user:
                return user
        self.log.error(f"{desired_user} is not part of the valid users form {users}. "
                       f"Check the 'accepted' users from {self.testing_page }")
        raise LoginPageException(f"{desired_user} is not a valid user")

    def write_credentials(self,
                          user: str,
                          password: str):
        """
        Writes the credentials in 'Username' and 'Password' fields.

        This method takes the parameters 'user' and 'password' and write
        them in their corresponding spaces.

        Args:
            user (str): User name
            password (str): corresponding password
        """
        def set_credentials(key, keys_value):
            """
            Set the specific credential, username or password, in the corresponding field.
            """
            self.set_element_value(self._get_element_params(key), keys_value)

        for key, keys_value in {"username": user, "password": password}.items():
            set_credentials(key, keys_value)

    def click_login_btn(self):
        """
        Clicks on the login button form login page.
        """
        self.click_on_element(self._get_element_params("login_bttn"))

    def login_page(self,
                   user=None,
                   password=None,
                   credentials=True):
        """
        Tries to logins.

        With the given 'user' and 'password' or not it tries to logins.

        Args:
            user (str:optional): User name
            password (str:optional): corresponding password
            credentials (bool:optional:default=True): Flag to try to login with or without
        """
        self.log.info("Tying to login")
        # Write credentials if it is requested
        if credentials:
            self.log.info(f"Writing credentials: user name {user}, password: {password}")
            self.write_credentials(user, password)
        # Click on login button
        self.click_login_btn()

    def get_login_error_text(self,
                             timeout: int=2):
        """
        Returns the text from error message.

        Returns:
            str: text from error message displayed after a wrong login.
        """
        return self.get_text_element(
            self._get_element_params(key="wrong_credential_error"),
            timeout=timeout
            )
