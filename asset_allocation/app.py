""" 
Application Aggregate 
Main entry point.
"""
from . import dal

class AppAggregate:
    """ Provides entry points to the application """
    def __init__(self):
        pass
    
    def create_asset_class(self, item: dal.AssetClass):
        """ Inserts the record """
        session = dal.get_session()
        session.add(item)
        session.commit()

    def save(self):
        """ Saves the entity """
        # session.commit()
        pass
