""" 
Application Aggregate 
Main entry point.
"""
#from . import dal
from .dal import AssetClass, AssetClassStock, get_session

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
        self.session = get_session()
        return self.session

    def save(self):
        """ Saves the entity """
        self.session.commit()
