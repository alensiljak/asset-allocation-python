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
from piecash import Book, Commodity, Price
from gnucash_portfolio.accounts import AccountAggregate, AccountsAggregate
from gnucash_portfolio.securities import SecurityAggregate, SecuritiesAggregate
from gnucash_portfolio.currencies import CurrencyAggregate


class AssetBase:
    """Base class for asset group & class"""
    def __init__(self):
        # reference to parent object
        self.parent: AssetClass = None

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

    @property
    def name(self):
        """Group name"""
        pass
        # if not self.data:
        #     return ""

        # if "name" in self.data:
        #     return self.data["name"]
        # else:
        #     return ""

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


class AssetGroup(AssetBase):
    """Group contains other groups or asset classes"""
    def __init__(self, json_node):
        super().__init__(json_node)
        self.classes = []


class AssetClass(AssetBase):
    """Asset Class contains stocks"""
    def __init__(self, json_node):
        super().__init__(json_node)

        # For cash asset class
        self.root_account = None

        self.stocks: List[Stock] = []
        # parse stocks
        if "stocks" not in json_node:
            return

        for symbol in json_node["stocks"]:
            stock = Stock(symbol)
            # todo add asset class allocation for this security.
            self.stocks.append(stock)


class Stock:
    """Stock link"""
    def __init__(self, symbol: str):
        """Parse json node"""
        self.symbol = symbol
        # Quantity (number of shares)
        self.quantity = Decimal(0)
        # Price (last known)
        self.price = Decimal(0)
        # Parent class
        self.parent = None

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
