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
        self.symbol = symbol
        # Quantity (number of shares)
        self.quantity = Decimal(0)
        # Price (last known)
        self.price = Decimal(0)
        # Parent class
        self.parent = None
        # Current allocation
        self.curr_alloc = Decimal(0)

    def __repr__(self):
        return f"<Stock (symbol='{self.symbol}')>"

    @property
    def value(self) -> Decimal:
        """Value of the shares. Value = Quantity * Price"""
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
        # parse stocks
        # if "stocks" not in json_node:
        #     return

        # for symbol in json_node["stocks"]:
        #     stock = Stock(symbol)
        #     # todo add asset class allocation for this security.
        #     self.stocks.append(stock)

    def __repr__(self):
        return f"<AssetClass (name='{self.name}',allocation='{self.allocation:.2f}')>"
        #,id='%s',allocation='%.2f',parent='%s')>" % (self.id, self.allocation, self.parentid)


class AssetAllocationModel:
    """ The container class """
    def __init__(self):
        self.total_amount: Decimal = Decimal(0)
        self.currency = None
        self.classes: List[AssetClass] = []

    def get_class_by_id(self, ac_id: int):
        """ Finds the asset class by id """
        assert isinstance(ac_id, int)

        # iterate recursively
        for ac in self.classes:
            result = self.__find(ac, ac_id)
            if result:
                return result
        # if nothing returned so far.
        return None

    def validate(self) -> bool:
        """ Validate that the values match """
        # TODO asset class allocation should match the sum of children's allocations
        # Each group should be compared.
        for ac in self.classes:
            pass

        return False

    def __find(self, root: AssetClass, ac_id: int):
        """ recursive function, searching for ac by id starting from the root """
        assert isinstance(root, AssetClass)
        assert isinstance(ac_id, int)

        result = None

        if root.id == ac_id:
            return root
        # Search through children
        for child in root.classes:
            result = self.__find(child, ac_id)
            if result:
                break
        return result
