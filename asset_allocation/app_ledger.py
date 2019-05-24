'''
    version of the app which is using ledger files
'''
from asset_allocation.loader_ledger import AssetAllocationLoaderLedger

class AppLedger:
    ''' The version of the application which uses ledger files '''

    def get_asset_allocation(self):
        ''' the main method '''
        loader = AssetAllocationLoaderLedger()
        model = loader.load_definition()
        return model
