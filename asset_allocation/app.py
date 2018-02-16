"""
Application Aggregate
Main entry point.
"""
from .dal import AssetClass, AssetClassStock, get_session
from .config import Config, ConfigKeys
from .loader import AssetAllocationLoader


class AppAggregate:
    """ Provides entry points to the application """
    def __init__(self):
        self.session = None
        # self.open_session()

    def create_asset_class(self, item: AssetClass):
        """ Inserts the record """
        session = self.open_session()
        session.add(item)
        session.commit()

    def delete(self, id: int):
        """ Delete asset class """
        assert isinstance(id, int)

        self.open_session()
        to_delete = self.get(id)
        self.session.delete(to_delete)
        self.save()

    def get(self, id: int) -> AssetClass:
        """ Loads Asset Class """
        self.open_session()
        item = self.session.query(AssetClass).filter(AssetClass.id == id).first()
        return item

    def open_session(self):
        """ Opens a db session and returns it """
        cfg = Config()
        db_path = cfg.get(ConfigKeys.asset_allocation_database_path)

        self.session = get_session(db_path)
        return self.session

    def save(self):
        """ Saves the entity """
        self.session.commit()

    def get_asset_allocation_model():
        """ Creates and populates the Asset Allocation model. The main function of the app. """
        # TODO: load from db
        loader = AssetAllocationLoader()
        model = loader.read_tree_from_db()

        # return the model for display
        return model
