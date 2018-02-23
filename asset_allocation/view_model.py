""" Asset Allocation view model """
from decimal import Decimal


class AssetAllocationViewModel:
    """ The view model for displaying Asset Allocation """
    def __init__(self):
        self.name = None
        
        self.set_allocation = Decimal(0)
        self.curr_allocation = Decimal(0)
        
        self.set_value = Decimal(0)
        self.curr_value = Decimal(0)
