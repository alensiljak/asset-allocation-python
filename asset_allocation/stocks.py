""" Operations on Stocks in GC book """
import os
from decimal import Decimal
from typing import List

from pkg_resources import Requirement, resource_filename

import piecash
from gnucash_portfolio.securities import SecuritiesAggregate, SecurityAggregate
from piecash import Book, Commodity, open_book
from pricedb import PriceModel, SecuritySymbol

from .config import Config, ConfigKeys


class StocksInfo:
    """
    Provides security information from GnuCash book.
    This is a proxy class to GC-Portfolio operations.
    """

    def __init__(self, config: Config = None):
        self.config = config if config else Config()
        # GnuCash db session/book.
        self.gc_book: Book = None
        # Prices session.
        self.pricedb_session = None
        self.logger = None

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

    def load_latest_price(self, symbol: SecuritySymbol) -> PriceModel:
        """ Loads the latest price for security """
        assert isinstance(symbol, SecuritySymbol)

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

            self.gc_book = open_book(gc_db, open_if_lock=True)
        return self.gc_book

    def get_symbols_with_positive_balances(self) -> List[str]:
        """ Identifies all the securities with positive balances """
        from gnucash_portfolio import BookAggregate

        holdings = []

        with BookAggregate() as book:
            # query = book.securities.query.filter(Commodity.)
            holding_entities = book.securities.get_all()
            for item in holding_entities:
                # Check holding balance
                agg = book.securities.get_aggregate(item)
                balance = agg.get_num_shares()
                if balance > Decimal(0):
                    holdings.append(f"{item.namespace}:{item.mnemonic}")
                else:
                    self.logger.debug(f"0 balance for {item}")
            # holdings = map(lambda x: , holding_entities)

        return holdings

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

    def __load_latest_prices_from_pricedb(self, symbol: SecuritySymbol) -> PriceModel:
        """
        Load security prices from PriceDb.
        Uses a separate price database that can be updated on (or from) Android.
        """
        from pricedb import PriceDbApplication

        assert isinstance(symbol, SecuritySymbol)

        session = self.__get_pricedb_session()
        price_db = PriceDbApplication(session)
        latest_price = price_db.get_latest_price(symbol)

        return latest_price

    def __get_pricedb_session(self):
        """ Provides initialization and access to module-level session """
        from pricedb import dal

        if not self.pricedb_session:
            self.pricedb_session = dal.get_default_session()
        return self.pricedb_session
