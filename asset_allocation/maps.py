"""
Maps between entities and model objects
"""
from . import dal, model


class AssetClassMapper():
    """ Maps the asset class record to the Asset Class object """
    def __init__(self):
        pass

    def map_entity(self, entity: dal.AssetClass):
        """ maps data from entity -> object """
        obj = model.AssetClass()

        obj.id = entity.id
        obj.parent_id = entity.parentid
        obj.name = entity.name
        obj.allocation = entity.allocation
        obj.sort_order = entity.sortorder
        #entity.stock_links
        #entity.diff_adjustment
        if entity.parentid == None:
            obj.depth = 0

        return obj

    # def entity_from_model(self, model: model.AssetClass):
    #     """ Populate entity from the model """


class ModelMapper():
    """ Maps the asset allocation model """
    def __init__(self, model: model.AssetAllocationModel):
        self.model = model

    def map_to_linear(self):
        """ Maps the tree to a linear representation suitable for display """
        pass
