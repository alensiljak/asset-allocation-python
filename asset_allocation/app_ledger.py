'''
    version of the app which is using ledger files
'''
from asset_allocation.loader_ledger import AssetAllocationLoaderLedger

class AppLedger:
    ''' The version of the application which uses ledger files '''

    def get_asset_allocation(self):
        ''' the main method '''
        loader = AssetAllocationLoaderLedger()
        # todo: load definition file
        definition = ""

        aa = loader.load_dictionary(definition)

        # todo validate: ac % must match the sum of it's children's.

        # todo load stock links: parse asset_allocation.ledger file

        return aa
