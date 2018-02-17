"""
Maps between entities and model objects
"""
from . import dal, model

class AssetClassMapper():
    """ Maps the asset class record to the Asset Class object """
    def __init__(self):
        pass

    def read_entity(self, entity: dal.AssetClass):
        """ maps data from entity -> object """
        obj = model.AssetClass()

        obj.id = entity.id
        obj.name = entity.name
        obj.allocation = entity.allocation

        return obj

    # def entity_from_model(self, model: model.AssetClass):
    #     """ Populate entity from the model """
