""" Operations on Stocks in GC book """
from decimal import Decimal
from logging import log, DEBUG
from piecash import Book, open_book, Price
from gnucash_portfolio.securities import SecuritiesAggregate, SecurityAggregate

from .config import Config, ConfigKeys

class StocksInfo:
    def __init__(self, config: Config):
        self.config = config
        # GnuCash db session/book.
        self.gc_book: Book = None
        # Prices session. For now, using GC for prices db.

    def load_stock_quantity(self, symbol: str) -> Decimal(0):
        """ retrieves stock quantity """
        book = self.get_gc_book()

        collection = SecuritiesAggregate(book)
        sec = collection.get_aggregate_for_symbol(symbol)
        quantity = sec.get_quantity()
        return quantity

    def load_latest_price(self, symbol: str) -> (Decimal, str):
        """ Loads the latest price for security """
        # For now, use GnuCash book. 
        # TODO use a separate price database that can be updated on Android
        book = self.get_gc_book()
        
        svc = SecuritiesAggregate(book)
        agg = svc.get_aggregate_for_symbol(symbol)
        if not agg:
            raise ValueError(f"Security not found {symbol}!")
        price: Price = agg.get_last_available_price()
        if not price:
            raise ValueError(f"Price not found for {symbol}!")
        return (price.value, price.currency.mnemonic)

    def get_gc_book(self):
        """ Returns the GnuCash db session """
        if not self.gc_book:
            gc_db = self.config.get(ConfigKeys.gnucash_book_path)
            if not gc_db:
                raise AttributeError("GnuCash book path not configured.")
            self.gc_book = open_book(gc_db)
        return self.gc_book