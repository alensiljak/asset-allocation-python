""" Operations with currencies """
from pricedb.repositories import PriceRepository
from pricedb import PriceDbApplication, PriceModel, SecuritySymbol


class CurrencyConverter:
    """ Convert between currencies """

    def __init__(self):
        self.rate: PriceModel = None

    def load_currency(self, mnemonic: str):
        """ load the latest rate for the given mnemonic; expressed in the base currency """
        # , base_currency: str <= ignored for now.
        if self.rate and self.rate.currency == mnemonic:
            # Already loaded.
            return

        app = PriceDbApplication()
        # TODO use the base_currency parameter for the query #33
        symbol = SecuritySymbol("CURRENCY", mnemonic)
        self.rate = app.get_latest_price(symbol)
        if not self.rate:
            raise ValueError(f"No rate found for {mnemonic}!")
