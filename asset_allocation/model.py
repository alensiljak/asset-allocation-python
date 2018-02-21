"""
Asset Allocation module. To be replaced by Asset-Allocation package.
"""
from decimal import Decimal
from typing import List
try: import simplejson as json
except ImportError: import json
import os
from os import path
from logging import log, DEBUG
# from piecash import Book, Commodity, Price
# from gnucash_portfolio.accounts import AccountAggregate, AccountsAggregate
# from gnucash_portfolio.securities import SecurityAggregate, SecuritiesAggregate
# from gnucash_portfolio.currencies import CurrencyAggregate


class _AssetBase:
    """Base class for asset group & class"""
    def __init__(self):
        # reference to parent object
        self.parent_id = None
        self.parent: AssetClass = None

        self.name = None
        # Set allocation %.
        self.allocation = Decimal(0)
        # if "allocation" in json_node:
        #     self.allocation = Decimal(json_node["allocation"])
        # else:
        self.allocation = Decimal(0)
        # How much is currently allocated, in %.
        self.curr_alloc = Decimal(0)
        # Difference between allocation and allocated.
        self.alloc_diff = Decimal(0)
        # Difference in percentages of allocation
        self.alloc_diff_perc = Decimal(0)

        # Current value in currency.
        self.alloc_value = Decimal(0)
        # Allocated value
        self.curr_value = Decimal(0)
        # Difference between allocation and allocated
        self.value_diff = Decimal(0)

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

    def __repr__(self):
        return f"<AssetClass (name='{self.name}',allocation='{self.allocation:.2f}')>"


class AssetAllocationModel:
    """ The container class """
    def __init__(self):
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
        # TODO asset class allocation should match the sum of children's allocations
        # Each group should be compared.
        for ac in self.classes:
            pass

        return False

    def calculate_totals(self):
        """ Add all the stock values and assign to the asset classes """
        # must be recursive
        total = Decimal(0)
        for ac in self.classes:
            self.__calculate_total(ac)
            total += ac.curr_value
        self.total_amount = total

    def __calculate_total(self, asset_class: AssetClass):
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
                self.__calculate_total(child)
                asset_class.curr_value += child.curr_value
