""" Tests for stocks operations """
from asset_allocation.stocks import StocksInfo

def test_value_reading(config):
    """ Retrieve value from GnuCash """
    unit = StocksInfo(config)
    value = unit.get_stock_quantity("ASX:VHY")

    assert value is not None
