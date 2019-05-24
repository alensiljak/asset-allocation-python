'''
Loader for ledger-style files.
'''
from .model import AssetAllocationModel, AssetClass, Stock, CashBalance


class AssetAllocationLoaderLedger:
    ''' Loader for ledger-style files. '''
    def __init__(self):
        self.model = None

    def load_definition(self):
        ''' load aa definition from a file '''
        self.model = AssetAllocationModel()
        
        return self.model
