""" Test Asset Allocation model classes """
from asset_allocation.models import AssetClass

def test_asset_class():
    """ test the model class """
    obj = AssetClass(None)
    #obj.name
    assert obj != None
