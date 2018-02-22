"""
Output formatters for the AA model
"""
from .model import AssetAllocationModel, AssetClass, Stock


class AsciiFormatter:
    """ Formats the model for the console output """

    def __init__(self):
        self.columns = [
            {"name": "Asset Class", "width": 25},
            {"name": "alloc.", "width": 5},
            {"name": "value", "width": 10}
        ]
        self.full = False

    def format(self, model: AssetAllocationModel, full: bool=False):
        """ Returns the view-friendly output of the aa model """
        self.full = full

        # Header
        output = f"Asset Allocation model, total: {model.currency} {model.total_amount:,.2f}\n"
        # Column Headers
        for column in self.columns:
            width = column["width"]
            output += f"{column['name']:^{width}}"
        output += "\n"
        output += f"---------------------------------------------------------------\n"

        # Asset classes
        for ac in model.classes:
            output += self.__get_ac_tree(ac)
        return output

    def __get_ac_tree(self, ac: AssetClass):
        """ formats the ac tree - entity with child elements """
        output = self.__get_ac_row(ac) + "\n"

        for child in ac.classes:
            output += self.__get_ac_tree(child)

        if self.full:
            for stock in ac.stocks:
                output += self.__get_stock_row(stock, ac.depth + 1) + "\n"

        return output

    def __get_ac_row(self, ac: AssetClass):
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


class HtmlFormatter:
    """ Formats HTML output """
    pass
