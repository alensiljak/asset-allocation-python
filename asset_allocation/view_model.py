""" Asset Allocation view model """
from decimal import Decimal


class AssetAllocationViewModel:
    """ The view model for displaying Asset Allocation """
    def __init__(self):
        # Depth / indentation level.
        self.depth = 0
        self.name = None
        
        self.set_allocation = Decimal(0)
        self.curr_allocation = Decimal(0)
        self.diff_allocation = Decimal(0)
        self.alloc_diff_perc = Decimal(0)
        
        self.set_value = Decimal(0)
        self.curr_value = Decimal(0)
        self.diff_value = Decimal(0)

        self.curr_value_own_currency = Decimal(0)
        self.own_currency = None

    def __repr__(self):
        return f"<AA Model ('{self.name}')>"
