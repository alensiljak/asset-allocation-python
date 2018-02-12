""" Configuration handling """
from configparser import ConfigParser
from logging import log, DEBUG

config_filename = "asset_allocation.cfg"

class Config:
    """ Reads and writes Asset Allocation config file """

    def __init__(self, ini_path=config_filename):
        # todo read the config file on creation
        # Where to expect it? In the same folder?
        self.config = ConfigParser()

    def print_all(self):
        """ Display all values """
        pass

    ###############
    # Private

    def __read_config(self):
        with open(config_filename) as cfg_file:
            content = cfg_file.read()

        log(DEBUG, "%s", content)
