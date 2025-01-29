"""
Contains common functions, constants, classes that can be util but not
necessary is part of a feature.
"""
import yaml
import requests
import random


class YamlManager:
    """
    Class which handle with yaml file stuff, as well load info, write, etc
    """

    @staticmethod
    def get_yaml_file_data(file_path):
        """Return a dictionary with the content from the given 'file_path' parameter"""
        content = {}
        with open(file_path, "r") as file:
            content = yaml.safe_load(file)
        return content


class ApiManagerError(Exception):
    """ApiManager Error"""


class ApiManager:
    """
    Static class to manage api requests
    """

    @staticmethod
    def get_api_response(url, timeout=5, is_random=False, num=1):
        """
        Methods to manage get api response

        Args:
            timeout(int/float): time out in seconds
            is_random(bool:optional): Flag to determinate to give a random user
            num(int:optional): Num of random data to return
        
        Returns:
            dict: Response from api
        """
        try:
            res = requests.get(url, timeout=timeout)
        except Exception as e:
            raise ApiManagerError("Unable to perform get request") from e
        if res.status_code == 200:
            if is_random:
                return random.choices(res.json(), k=num)
            return res.json()
        raise ApiManagerError("Error request")
