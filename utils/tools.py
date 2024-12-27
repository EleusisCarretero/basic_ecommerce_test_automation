import yaml


class YamlManager:

    @staticmethod
    def get_yaml_file_data(file_path):
        content = {}
        with open(file_path, "r") as file:
            content = yaml.safe_load(file)
        return content
