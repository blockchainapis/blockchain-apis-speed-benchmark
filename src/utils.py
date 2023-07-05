import yaml

from yaml.loader import SafeLoader

from src.Types import Config


def load_config(path: str) -> Config:
    """Load the configuration file from the given path.
    
    It just load the Yaml dictionary and returns it

    :param path: The path towards the configuration file
    :type path: str
    :return: The Config file
    :rtype: Config
    """
    with open(path, "r") as f:
        return yaml.load(f, Loader=SafeLoader)

