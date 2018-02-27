""" Operations with currencies """
from pricedb.repositories import PriceRepository
from pricedb import PriceDbApplication


class CurrencyConverter:
    """ Convert between currencies """
    def __init__(self):
        self.rate = None

    def load_currency(self, mnemonic: str):
        """ load the latest rate for the currency """
        # , base_currency: str <= ignored for now.
        app = PriceDbApplication()
        # TODO use the base_currency parameter for the query #33
        self.rate = app.get_latest_price("CURRENCY", mnemonic)
        if not self.rate:
            raise ValueError(f"No rate found for {mnemonic}!")
