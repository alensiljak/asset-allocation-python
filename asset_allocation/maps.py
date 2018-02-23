"""
Maps between entities and model objects
"""
from . import dal, model
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

    # def entity_from_model(self, model: model.AssetClass):
    #     """ Populate entity from the model """


class ModelMapper():
    """ Maps the asset allocation model """
    def __init__(self, model: model.AssetAllocationModel):
        self.model = model

    def map_to_linear(self, with_stocks: bool=False):
        """ Maps the tree to a linear representation suitable for display """
        result = []

        for ac in self.model.classes:
            row = self.__get_ac_tree(ac, with_stocks)

    def __get_ac_tree(self, ac: model.AssetClass, with_stocks: bool):
        """ formats the ac tree - entity with child elements """
        output = self.__get_ac_row(ac) + "\n"

        for child in ac.classes:
            output += self.__get_ac_tree(child)

        if with_stocks:
            for stock in ac.stocks:
                output += self.__get_stock_row(stock, ac.depth + 1) + "\n"

        return output

    def __get_ac_row(self, ac: model.AssetClass):
        """ Formats one Asset Class record """
        output = ""

        # Name
        name_col = ac.name
        # Indent according to depth.
        for _ in range(0, ac.depth):
            name_col = f"    {name_col}"

        width = self.columns[0]["width"]
        output += f"{name_col:<{width}}: "

        allocation = f"{ac.allocation:.2f}"
        output += f"{allocation:>5}"

        # value
        value = f"{ac.curr_value:,.0f}"
        output += f"{value:>9}"

        # https://en.wikipedia.org/wiki/ANSI_escape_code
        # CSI="\x1B["
        # # red = 31, green = 32
        # output += CSI+"31;40m" + "Colored Text" + CSI + "0m"

        return output

    def __get_stock_row(self, stock: Stock, depth: int) -> str:
        """ formats stock row """
        output = ""

        # Symbol
        name_col = stock.symbol
        for _ in range(0, depth):
            name_col = f"    {name_col}"
        width = self.columns[0]["width"]
        output += f"{name_col:<{width}}: "

        # Current allocation
        allocation = f"{stock.curr_alloc:.2f}"
        output += f"{allocation:>5}"

        # Value in base currency
        value = f"{stock.value_in_base_currency:,.0f}"
        output += f"{value:>9}"

        # Value in security's currency.
        value = f"({stock.value:,.0f}"
        output += f"{value:>8}"

        output += f" {stock.currency}"
        output += ")"

        return output
