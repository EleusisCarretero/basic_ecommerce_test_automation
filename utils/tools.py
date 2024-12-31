"""
Contains common functions, constants, classes that can be util but not
necessary is part of a feature.
"""
import yaml


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
