""" Test the configuration mechanism """

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
    content = cfg.print_all()

    assert content is not None

def test_create_config():
    """ create a config file. Incomplete! """
    cfg = ConfigParser()
    cfg.add_section("one")
    cfg.set("one", "blah", "yo!")
    #cfg.write()
