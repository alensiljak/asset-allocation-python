""" Configuration handling """
from configparser import ConfigParser
from logging import log, DEBUG, ERROR
import io
import os.path
from pkg_resources import Requirement, resource_filename


config_filename = "data/asset_allocation.ini"

class Config:
    """ Reads and writes Asset Allocation config file """

    def __init__(self, ini_path: str = None):
        # todo read the config file on creation
        # Where to expect it? In the same folder?
        self.config = ConfigParser()
        self.__read_config(ini_path)

    def print_all(self):
        """ Display all values """
        in_memory = io.StringIO("")
        self.config.write(in_memory)
        content = in_memory.read()
        log(DEBUG, "config content: %s", content)
        in_memory.close()
        return content

    def __read_config(self, ini_path: str):
        """ Read the config file """
        if ini_path:
            # file_path = os.path.relpath(ini_path)
            file_path = os.path.abspath(ini_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError("File path not found: %s", file_path)
        else:
            # file_path = os.path.relpath(config_filename)
            file_path = self.get_config_path()
        # check if file exists
        if not os.path.isfile(file_path):
            log(ERROR, "file not found: %s", file_path)
            raise FileNotFoundError("configuration file not found %s", file_path)

        #log(DEBUG, "using config file %s", file_path )
        with open(file_path) as cfg_file:
            self.config.read_file(cfg_file)

    def get_config_path(self) -> str:
        """ gets the default config path from resources """
        filename = resource_filename(Requirement.parse("Asset-Allocation"), config_filename)
        return filename
