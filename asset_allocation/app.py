"""
Application Aggregate
Main entry point.
"""
from typing import List

from .config import Config, ConfigKeys
from .dal import AssetClass, AssetClassStock
from .loader import AssetAllocationLoader
from .model import AssetAllocationModel


class AppAggregate:
    """ Provides entry points to the application """

    def __init__(self):
        self.session = None
        self.logger = None

    def create_asset_class(self, item: AssetClass):
        """ Inserts the record """
        session = self.open_session()
        session.add(item)
        session.commit()

    def add_stock_to_class(self, assetclass_id: int, symbol: str):
        """ Add a stock link to an asset class """
        assert isinstance(symbol, str)
        assert isinstance(assetclass_id, int)

        item = AssetClassStock()
        item.assetclassid = assetclass_id
        item.symbol = symbol

        session = self.open_session()
        session.add(item)
        self.save()

        return item

    def delete(self, id: int):
        """ Delete asset class """
        assert isinstance(id, int)

        self.open_session()
        to_delete = self.get(id)
        self.session.delete(to_delete)
        self.save()

    def find_unallocated_holdings(self):
        """ Identifies any holdings that are not included in asset allocation """
        # Get linked securities
        session = self.open_session()
        linked_entities = session.query(AssetClassStock).all()
        linked = []
        # linked = map(lambda x: f"{x.symbol}", linked_entities)
        for item in linked_entities:
            linked.append(item.symbol)

        # Get all securities with balance > 0.
        from .stocks import StocksInfo

        stocks = StocksInfo()
        stocks.logger = self.logger
        holdings = stocks.get_symbols_with_positive_balances()

        # Find those which are not included in the stock links.
        non_alloc = []
        index = -1
        for item in holdings:
            try:
                index = linked.index(item)
                self.logger.debug(index)
            except ValueError:
                non_alloc.append(item)

        return non_alloc

    def get(self, id: int) -> AssetClass:
        """ Loads Asset Class """
        self.open_session()
        item = self.session.query(AssetClass).filter(
            AssetClass.id == id).first()
        return item

    def open_session(self):
        """ Opens a db session and returns it """
        from .dal import get_session

        cfg = Config()
        cfg.logger = self.logger
        db_path = cfg.get(ConfigKeys.asset_allocation_database_path)

        self.session = get_session(db_path)
        return self.session

    def save(self):
        """ Saves the entity """
        self.session.commit()

    def get_asset_allocation(self):
        """ Creates and populates the Asset Allocation model. The main function of the app. """
        # load from db
        # TODO set the base currency
        base_currency = "EUR"

        loader = AssetAllocationLoader(base_currency=base_currency)
        loader.logger = self.logger
        model = loader.load_tree_from_db()

        model.validate()

        # securities
        # read stock links
        loader.load_stock_links()
        # read stock quantities from GnuCash
        loader.load_stock_quantity()
        # Load cash balances
        loader.load_cash_balances()
        # loader.session
        # read prices from Prices database
        loader.load_stock_prices()
        # recalculate stock values into base currency
        loader.recalculate_stock_values_into_base()
        # calculate
        model.calculate_current_value()
        model.calculate_set_values()
        model.calculate_current_allocation()

        # return the model for display
        return model

    def get_asset_classes_for_security(self, namespace: str, symbol: str) -> List[AssetClass]:
        """ Find all asset classes (should be only one at the moment, though!) to which the symbol belongs """
        full_symbol = symbol
        if namespace:
            full_symbol = f"{namespace}:{symbol}"

        query = (
            self.session.query(AssetClassStock)
                .filter(AssetClassStock.symbol == full_symbol)
        )
        result = query.all()
        return result

    def validate_model(self):
        """ Validate the model """
        model: AssetAllocationModel = self.get_asset_allocation_model()
        model.logger = self.logger

        valid = model.validate()
        if valid:
            print(f"The model is valid. Congratulations")
        else:
            print(f"The model is invalid.")

    def export_symbols(self):
        """ Exports all used symbols """
        session = self.open_session()
        links = session.query(AssetClassStock).order_by(
            AssetClassStock.symbol).all()
        output = []
        for link in links:
            output.append(link.symbol + '\n')

        # Save output to a text file.
        with open("symbols.txt", mode='w') as file:
            file.writelines(output)

        print("Symbols exported to symbols.txt")
