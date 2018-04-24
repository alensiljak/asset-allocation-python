"""
Maps between entities and model objects
"""
from . import dal, model
from .model import Stock, CashBalance
from .view_model import AssetAllocationViewModel


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


class ModelMapper():
    """ Maps the asset allocation model to various other representations. """
    def __init__(self, model: model.AssetAllocationModel):
        self.model = model

    def map_to_linear(self, with_stocks: bool=False):
        """ Maps the tree to a linear representation suitable for display """
        result = []

        for ac in self.model.classes:
            rows = self.__get_ac_tree(ac, with_stocks)
            result += rows
        return result

    def __get_ac_tree(self, ac: model.AssetClass, with_stocks: bool):
        """ formats the ac tree - entity with child elements """
        output = []
        output.append(self.__get_ac_row(ac))

        for child in ac.classes:
            output += self.__get_ac_tree(child, with_stocks)

        if with_stocks:
            for stock in ac.stocks:
                row = None
                if isinstance(stock, Stock):
                    row = self.__get_stock_row(stock, ac.depth + 1)
                elif isinstance(stock, CashBalance):
                    row = self.__get_cash_row(stock, ac.depth + 1)
                output.append(row)

        return output

    def __get_ac_row(self, ac: model.AssetClass) -> AssetAllocationViewModel:
        """ Formats one Asset Class record """
        view_model = AssetAllocationViewModel()

        view_model.depth = ac.depth
        
        # Name
        view_model.name = ac.name

        view_model.set_allocation = ac.allocation
        view_model.curr_allocation = ac.curr_alloc
        view_model.diff_allocation = ac.alloc_diff
        view_model.alloc_diff_perc = ac.alloc_diff_perc

        # value
        view_model.curr_value = ac.curr_value
        # expected value
        view_model.set_value = ac.alloc_value
        # diff
        view_model.diff_value = ac.value_diff

        return view_model

    def __get_stock_row(self, stock: Stock, depth: int) -> str:
        """ formats stock row """
        assert isinstance(stock, Stock)

        view_model = AssetAllocationViewModel()

        view_model.depth = depth

        # Symbol
        view_model.name = stock.symbol

        # Current allocation
        view_model.curr_allocation = stock.curr_alloc

        # Value in base currency
        view_model.curr_value = stock.value_in_base_currency

        # Value in security's currency.
        view_model.curr_value_own_currency = stock.value
        view_model.own_currency = stock.currency

        return view_model

    def __get_cash_row(self, item: CashBalance, depth: int) -> str:
        """ formats stock row """
        assert isinstance(item, CashBalance)

        view_model = AssetAllocationViewModel()

        view_model.depth = depth

        # Symbol
        view_model.name = item.symbol

        # Value in base currency
        view_model.curr_value = item.value_in_base_currency

        # Value in security's currency.
        view_model.curr_value_own_currency = item.value
        view_model.own_currency = item.currency

        return view_model
