""" 
Configuration handling 
The config file is stored in data directory and is located by using Resources.
Ref: http://peak.telecommunity.com/DevCenter/setuptools#non-package-data-files
"""
from configparser import ConfigParser
from logging import log, DEBUG, ERROR
import io
import os.path
import shutil
from pkg_resources import Requirement, resource_filename


config_filename = "asset_allocation.ini"
#config_filename = "data/asset_allocation.ini"

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

    def delete_user_config(self):
        """ Delete current user's config file """
        file = self.get_config_path()
        os.remove(file)

    def __read_config(self, ini_path: str):
        """ Read the config file """
        if ini_path:
            # file_path = os.path.relpath(ini_path)
            file_path = os.path.abspath(ini_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError("File path not found: %s", file_path)
        else:
            file_path = self.get_config_path()
            # copy the template if file does not yet exist
            if not os.path.exists(file_path):
                self.__create_user_config()
        
        # check if file exists
        if not os.path.isfile(file_path):
            log(ERROR, "file not found: %s", file_path)
            raise FileNotFoundError("configuration file not found %s", file_path)

        #log(DEBUG, "using config file %s", file_path )
        contents = self.get_contents(file_path)
        self.config.read_string(contents)

    def __get_config_template_path(self) -> str:
        """ gets the default config path from resources """
        filename = resource_filename(Requirement.parse("Asset-Allocation"), 
                                     "data/" + config_filename)
        return filename

    def __get_user_path(self) -> str:
        """ Returns the current user's home directory """
        return os.path.expanduser("~")

    def __create_user_config(self):
        """ Copy the config template into user's directory """
        src_path = self.__get_config_template_path()
        src = os.path.abspath(src_path)
        if not os.path.exists(src):
            log(ERROR, "Config template not found %s", src)
            raise FileNotFoundError()

        dst = os.path.abspath(self.get_config_path())

        shutil.copyfile(src, dst)

        if not os.path.exists(dst):
            raise FileNotFoundError("Config file could not be copied to user dir!")

    def get_config_path(self) -> str:
        """ Returns the path where the active config file is expected """
        dst_dir = self.__get_user_path()
        dst = dst_dir + "/" + config_filename
        return dst

    def get_contents(self, file_path) -> str:
        """ Reads the contents of the config file """
        contents = None
        with open(file_path) as cfg_file:
            contents = cfg_file.read()
        return contents