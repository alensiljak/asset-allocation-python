'''
Test the new version of Asset Allocation, using the text file for the definition,
and ledger output for the current state.
'''
from asset_allocation.app_ledger import AppLedger
from asset_allocation.loader_ledger import AssetAllocationLoaderLedger


def test_read_definition(aa_definition):
    ''' Read the definition from the file '''
    # app = AppLedger()
    # app.get_asset_allocation()
    test_obj = AssetAllocationLoaderLedger()
    actual = test_obj.load_definition(aa_definition)

    assert actual is not None

def test_load_dict(aa_definition):
    ''' parse into dictionary '''
    test_obj = AssetAllocationLoaderLedger()
    actual = test_obj.load_dictionary(aa_definition)

    assert actual is not None
