""" Configuration handling """
from configparser import ConfigParser
from logging import log, DEBUG
import io
import os.path

config_filename = "asset_allocation.cfg"

class Config:
    """ Reads and writes Asset Allocation config file """

    def __init__(self, ini_path=config_filename):
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

    def __read_config(self, ini_path):
        """ Read the config file """
        if ini_path:
            file_path = os.path.relpath(ini_path)
            abs_path = os.path.abspath(ini_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError("File path not found: %s", file_path)
        else:
            file_path = os.path.relpath(config_filename)
        # check if file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError("configuration file not found %s", file_path)

        self.config.read_file(file_path)
