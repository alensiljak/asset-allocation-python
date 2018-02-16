""" Test Asset Allocation model classes """
from asset_allocation.model import AssetClass

def test_asset_class():
    """ test the model class """
    obj = AssetClass()
    #obj.name
    assert obj != None
