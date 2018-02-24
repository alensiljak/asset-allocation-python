"""
Output formatters for the AA model
"""
from .model import AssetAllocationModel, AssetClass, Stock
from .maps import ModelMapper
from .view_model import AssetAllocationViewModel


class AsciiFormatter:
    """ Formats the model for the console output """

    def __init__(self):
        self.columns = [
            {"name": "Asset Class", "width": 25},
            {"name": "alloc.", "width": 5},
            {"name": "value", "width": 10},
            {"name": "al.val.", "width": 8}
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

        view_model = ModelMapper(model).map_to_linear(self.full)
        for row in view_model:
            output += self.__format_row(row) + "\n"
        
        return output

    def __format_row(self, row: AssetAllocationViewModel):
        """ display-format one row """
        """ Formats one Asset Class record """
        output = ""

        # Name
        name_col = row.name
        # Indent according to depth.
        for _ in range(0, row.depth):
            name_col = f"    {name_col}"

        width = self.columns[0]["width"]
        output += f"{name_col:<{width}}: "

        # Set Allocation
        allocation = ""
        if row.set_allocation:
            allocation = f"{row.set_allocation:.2f}"
        output += f"{allocation:>5}"

        # value
        value = f"{row.curr_value:,.0f}"
        output += f"{value:>9}"

        # Value in security's currency.
        value = ""
        if row.curr_value_own_currency:
            value = f"({row.curr_value_own_currency:,.0f}"
            value += f" {row.own_currency}"
            value += ")"
        output += f"{value:>13}"
        
        # Set value
        set_value = f"{row.set_value:.2f}"
        output += f"{set_value:>6}"

        # https://en.wikipedia.org/wiki/ANSI_escape_code
        # CSI="\x1B["
        # # red = 31, green = 32
        # output += CSI+"31;40m" + "Colored Text" + CSI + "0m"

        return output


class HtmlFormatter:
    """ Formats HTML output """
    pass
