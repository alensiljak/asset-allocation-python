""" Operations on Stocks in GC book """
from decimal import Decimal
from logging import log, DEBUG
from piecash import Book, open_book
from gnucash_portfolio.securities import SecuritiesAggregate, SecurityAggregate

from .config import Config, ConfigKeys

class StocksInfo:
    def __init__(self, config: Config):
        self.config = config

    def get_stock_quantity(self, symbol: str) -> Decimal(0):
        """ retrieves stock quantity """
        # TODO read config value for GC book
        config = self.config
        gc_db = config.get(ConfigKeys.gnucash_book_path)
        if not gc_db:
            raise AttributeError("GnuCash book path not configured.")
        # log(DEBUG, f"using GC book: {gc_db}.")
        
        with open_book(gc_db) as book:
            collection = SecuritiesAggregate(book)
            sec = collection.get_aggregate_for_symbol(symbol)
            # TODO use the aa currency
            value = sec.get_value()
            return value
