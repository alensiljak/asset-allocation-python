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

    def get(self, id: int):
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
