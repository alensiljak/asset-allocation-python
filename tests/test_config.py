""" Test the configuration mechanism """

import os
from logging import log, DEBUG
from asset_allocation.config import Config
from configparser import ConfigParser

def test_get_config_location():
    """ Get the config location from setuptools """
    cfg = Config()
    filename = cfg.get_config_path()
    assert "asset_allocation.ini" in filename

def test_config_read():
    """ Read config file """
    cfg = Config("../data/asset_allocation.ini")
    content = cfg.get_contents()

    assert content is not None

def test_create_config():
    """ create a config file. Incomplete! """
    cfg = ConfigParser()
    cfg.add_section("one")
    cfg.set("one", "blah", "yo!")
    #cfg.write()

def test_locating_user_dir():
    """ Locate user directory, for storing the config file """
    user_path1 = os.path.expanduser("~")
    # user_path2 = os.path.expanduser("~user")
    # print(user_path1)
    log(DEBUG, "%s", user_path1)
    assert user_path1 == "yo"
    # assert user_path2 == "yo"

def test_user_config_created():
    """ test if the user configuration instance is created """
    cfg = Config()
    ini_path = cfg.get_config_path()
    assert ini_path is not None
