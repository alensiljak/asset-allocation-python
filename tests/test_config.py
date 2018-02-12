""" Test the configuration mechanism """

from asset_allocation.config import Config

def test_config_read():
    """ Read config file """
    cfg = Config("data/asset_allocation.cfg")
    content = cfg.print_all()

    assert content is not None
