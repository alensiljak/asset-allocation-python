"""
Asset Allocation module.
"""
import os
import logging
from decimal import Decimal
from logging import DEBUG, log
from os import path
from typing import List

try: import simplejson as json
except ImportError: import json


class _AssetBase:
    """Base class for asset group & class"""
    def __init__(self):
        # reference to parent object
        self.parent_id = None
        self.parent: AssetClass = None

        self.name = None
        # Set allocation %.
        self.allocation = Decimal(0)
        # How much is currently allocated, in %.
        self.curr_alloc = Decimal(0)
        # Difference between allocation and allocated.
        # self.alloc_diff = Decimal(0)
        # Difference in percentages of allocation
        # self.alloc_diff_perc = Decimal(0)

        # Current value in currency.
        self.alloc_value = Decimal(0)
        # Allocated value
        self.curr_value = Decimal(0)
        # Difference between allocation and allocated
        #self.value_diff = Decimal(0)

        # Threshold. Expressed in %.
        self.threshold = Decimal(0)
        self.over_threshold = False
        self.under_threshold = False

        # view-related
        # Order of child classes within an asset class group.
        self.sort_order = None
        # Depth level within an asset class tree
        self.depth = 0

    @property
    def alloc_diff(self):
        """ The difference between set allocation and current allocation """
        return self.curr_alloc - self.allocation

    @property
    def alloc_diff_perc(self):
        """ The difference in current allocation vs set allocation expressed as 
        a percentage """
        return self.alloc_diff * 100 / self.allocation

    @property
    def value_diff(self):
        """ The difference between set value and current value. """
        return self.curr_value - self.alloc_value

    @property
    def fullname(self):
        """ includes the full path with parent names """
        prefix = ""
        if self.parent:
            if self.parent.fullname:
                prefix = self.parent.fullname + ":"
        else:
            # Only the root does not have a parent. In that case we also don't need a name.
            return ""

        return prefix + self.name


class CashBalance:
    """ Similar to Stock but keeps track of cash balance per currency """
    def __init__(self, symbol: str):
        self.symbol: str = symbol
        # Own currency
        self.currency: str = None
        # Value in own currency
        self.value: Decimal = None
        # Value in base currency
        self.value_in_base_currency: Decimal = None

    def __repr__(self):
        return f"<Cash (symbol='{self.symbol}',value={self.value} {self.currency},({self.value_in_base_currency}))>"


class Stock:
    """Stock link"""
    def __init__(self, symbol: str):
        self.symbol: str = symbol
        # Quantity (number of shares)
        self.quantity: Decimal = Decimal(0)
        # Price (last known)
        self.price: Decimal = Decimal(0)
        # Currency symbol for the price
        self.currency: str = None
        # Parent class
        self.parent: AssetClass = None
        # Value in base currency. Calculated externally.
        self.value_in_base_currency: Decimal = None
        # Current allocation
        self.curr_alloc: Decimal = Decimal(0)

    def __repr__(self):
        return f"<Stock (symbol='{self.symbol}',quantity={self.quantity},value={self.value})>"

    @property
    def value(self) -> Decimal:
        """
        Value of the holdings in exchange currency.
        Value = Quantity * Price
        """
        assert isinstance(self.price, Decimal)
        
        return self.quantity * self.price

    @property
    def asset_class(self) -> str:
        """ Returns the full asset class path for this stock """
        result = self.parent.name if self.parent else ""
        # Iterate to the top asset class and add names.
        cursor = self.parent
        while cursor:
            result = cursor.name + ":" + result
            cursor = cursor.parent
        return result


class AssetClass(_AssetBase):
    """Asset Class contains stocks """
    def __init__(self):
        super().__init__()

        self.id = None

        # For cash asset class
        self.root_account = None

        # It can contain only other classes OR stocks, not both at the same time!
        self.classes = []
        self.stocks: List[Stock] = []

    @property
    def child_allocation(self):
        """ The sum of all child asset classes' allocations """
        sum = Decimal(0)
        if self.classes:
            for child in self.classes:
                sum += child.child_allocation
        else:
            # This is not a branch but a leaf. Return own allocation.
            sum = self.allocation

        return sum

    def __repr__(self):
        return f"<AssetClass (name='{self.name}',allocation='{self.allocation:.2f}')>"


class AssetAllocationModel:
    """ The container class """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.total_amount: Decimal = Decimal(0)
        self.currency = None
        # Child classes, the first-level only. This is the beginning of the tree.
        self.classes: List[AssetClass] = []
        
        # Index of all asset classes. Linear representation.
        self.asset_classes: List[AssetClass] = []
        # Index of all Stocks
        self.stocks: List[Stock] = []

    def get_class_by_id(self, ac_id: int) -> AssetClass:
        """ Finds the asset class by id """
        assert isinstance(ac_id, int)

        # iterate recursively
        for ac in self.asset_classes:
            if ac.id == ac_id:
                return ac
        # if nothing returned so far.
        return None

    def get_cash_asset_class(self) -> AssetClass:
        """ Find the cash asset class by name. """
        for ac in self.asset_classes:
            if ac.name.lower() == "cash":
                return ac
        return None

    def validate(self) -> bool:
        """ Validate that the values match. Incomplete! """
        # Asset class allocation should match the sum of children's allocations.
        # Each group should be compared.
        sum = Decimal(0)

        # Go through each asset class, not just the top level.
        for ac in self.asset_classes:
            if ac.classes:
                # get the sum of all the children's allocations
                child_alloc_sum = ac.child_allocation
                # compare to set allocation
                if ac.allocation != child_alloc_sum:
                    message = f"The sum of child allocations {child_alloc_sum:.2f} invalid for {ac}!"
                    self.logger.warning(message)
                    print(message)
                    return False

        # also make sure that the sum of 1st level children matches 100
        for ac in self.classes:
            sum += ac.allocation
        if sum != Decimal(100):
            message = f"The sum of all allocations ({sum:.2f}) does not equal 100!"
            self.logger.warning(message)
            print(message)
            return False

        return True

    def calculate_set_values(self):
        """ Calculate the expected totals based on set allocations """
        for ac in self.asset_classes:
            ac.alloc_value = self.total_amount * ac.allocation / Decimal(100)

    def calculate_current_allocation(self):
        """ Calculates the current allocation % based on the value """
        for ac in self.asset_classes:
            ac.curr_alloc = ac.curr_value * 100 / self.total_amount

    def calculate_current_value(self):
        """ Add all the stock values and assign to the asset classes """
        # must be recursive
        total = Decimal(0)
        for ac in self.classes:
            self.__calculate_current_value(ac)
            total += ac.curr_value
        self.total_amount = total

    def __calculate_current_value(self, asset_class: AssetClass):
        """ Calculate totals for asset class by adding all the children values """
        # Is this the final asset class, the one with stocks?
        if asset_class.stocks:
            # add all the stocks
            stocks_sum = Decimal(0)
            for stock in asset_class.stocks:
                # recalculate into base currency!
                stocks_sum += stock.value_in_base_currency

            asset_class.curr_value = stocks_sum

        if asset_class.classes:
            # load totals for child classes
            for child in asset_class.classes:
                self.__calculate_current_value(child)
                asset_class.curr_value += child.curr_value
