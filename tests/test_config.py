""" Test the configuration mechanism """

from asset_allocation.config import Config


def test_get_config_location():
    """ Get the config location from setuptools """
    cfg = Config()
    filename = cfg.get_config_path()
    assert filename == "asset_allocation.cfg"

def test_config_read():
    """ Read config file """
    cfg = Config("../data/asset_allocation.cfg")
    content = cfg.print_all()

    assert content is not None

# def test_create_config():
#     """ create a config file """
#     cfg = con
