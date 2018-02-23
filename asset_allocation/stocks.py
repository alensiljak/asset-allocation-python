""" Operations on Stocks in GC book """
import os
from decimal import Decimal
from logging import DEBUG, log
from pkg_resources import Requirement, resource_filename

import piecash
from gnucash_portfolio.securities import SecuritiesAggregate, SecurityAggregate
from piecash import Book, open_book
from pricedb.model import PriceModel

from .config import Config, ConfigKeys


class StocksInfo:
    def __init__(self, config: Config):
        self.config = config
        # GnuCash db session/book.
        self.gc_book: Book = None
        # Prices session.
        self.pricedb_session = None

    def close_databases(self):
        """ Close all database sessions """
        if self.gc_book:
            self.gc_book.close()
        if self.pricedb_session:
            self.pricedb_session.close()

    def load_stock_quantity(self, symbol: str) -> Decimal(0):
        """ retrieves stock quantity """
        book = self.get_gc_book()

        collection = SecuritiesAggregate(book)
        sec = collection.get_aggregate_for_symbol(symbol)
        quantity = sec.get_quantity()
        return quantity

    def load_latest_price(self, symbol: str) -> PriceModel:
        """ Loads the latest price for security """
        # result = self.__load_latest_prices_from_gnucash(symbol)
        result = self.__load_latest_prices_from_pricedb(symbol)
        return result

    def get_gc_book(self):
        """ Returns the GnuCash db session """
        if not self.gc_book:
            gc_db = self.config.get(ConfigKeys.gnucash_book_path)
            if not gc_db:
                raise AttributeError("GnuCash book path not configured.")
            # check if this is the abs file exists
            if not os.path.isabs(gc_db):
                gc_db = resource_filename(Requirement.parse("Asset-Allocation"), gc_db)
                if not os.path.exists(gc_db):
                    raise ValueError(f"Invalid GnuCash book path {gc_db}")
            
            self.gc_book = open_book(gc_db)
        return self.gc_book
    
    def __load_latest_prices_from_gnucash(self, symbol):
        """ Load security prices from GnuCash book. Deprecated. """
        book = self.get_gc_book()
        
        svc = SecuritiesAggregate(book)
        agg = svc.get_aggregate_for_symbol(symbol)
        if not agg:
            raise ValueError(f"Security not found {symbol}!")
        price: piecash.Price = agg.get_last_available_price()
        if not price:
            raise ValueError(f"Price not found for {symbol}!")
        
        # Map to price model.
        result = PriceModel()
        result.value = price.value
        result.currency = price.currency.mnemonic
        return result

    def __load_latest_prices_from_pricedb(self, symbol: str) -> PriceModel:
        """
        Load security prices from PriceDb.
        Uses a separate price database that can be updated on (or from) Android.
        """
        from pricedb import app
        # from pricedb.model import Price

        namespace = None
        mnemonic = symbol
        symbol_parts = symbol.split(":")
        if len(symbol_parts) > 1:
            namespace = symbol_parts[0]
            mnemonic = symbol_parts[1]

        session = self.__get_pricedb_session()
        pricedb = app.PriceDbApplication(session)
        latest_price = pricedb.get_latest_price(namespace, mnemonic)

        return latest_price

    def __get_pricedb_session(self):
        """ Provides initialization and access to module-level session """
        from pricedb import dal

        if not self.pricedb_session:
            self.pricedb_session = dal.get_default_session()
        return self.pricedb_session
