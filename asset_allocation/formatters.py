"""
Output formatters for the AA model
"""
from .model import AssetAllocationModel, AssetClass, Stock


class AsciiFormatter:
    """ Formats the model for the console output """
    def __init__(self):
        self.columns = [ 
            { "name": "Asset Class", "width": 25 }, 
            { "name": "allocation", "width": 5 },
            { "name": "value", "width": 10 }
        ]
        self.full = False

    def format(self, model: AssetAllocationModel, full: bool=False):
        """ Returns the view-friendly output of the aa model """
        self.full = full

        # Header
        output = f"Asset Allocation model, total: {model.currency} {model.total_amount:,.2f}\n"
        # Columns
        for column in self.columns:
            width = column["width"]
            output += f"{column['name']:^{width}}"
        output += "\n"

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
        # Indent according to depth.
        for _ in range(0, ac.depth):
            output = f"    {output}"
        
        width = self.columns[0]["width"]
        output += f"{ac.name:<{width}}: "
        
        allocation = f"{ac.allocation:.2f}"
        output += f"{allocation:>5}"

        # value
        value = f"{ac.curr_value:,.0f}"
        output += f"{value:>10}"

        # https://en.wikipedia.org/wiki/ANSI_escape_code
        # CSI="\x1B["
        # # red = 31, green = 32
        # output += CSI+"31;40m" + "Colored Text" + CSI + "0m"
        
        return output

    def __get_stock_row(self, stock: Stock, depth: int) -> str:
        """ formats stock row """
        output = ""
        for _ in range(0, depth):
            output += "    "
        width = self.columns[0]["width"]
        output += f"{stock.symbol:<{width}}: "

        #stock.
        allocation = f"{stock.curr_alloc:.2f}"
        output += f"{allocation:>5}"

        value = f"{stock.value:,.0f}"
        output += f"{value:>8}"

        output += f" {stock.currency}"

        return output


class HtmlFormatter:
    """ Formats HTML output """
    pass
    