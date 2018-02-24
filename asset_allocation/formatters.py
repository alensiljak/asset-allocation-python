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
            {"name": "value", "width": 9},
            {"name": "loc.cur.", "width": 13},
            {"name": "al.val.", "width": 8},
            {"name": "diff", "width": 8}
        ]
        self.full = False

    def format(self, model: AssetAllocationModel, full: bool=False):
        """ Returns the view-friendly output of the aa model """
        self.full = full

        # Header
        output = f"Asset Allocation model, total: {model.currency} {model.total_amount:,.2f}\n"

        # Column Headers
        for column in self.columns:
            name = column['name']
            if not self.full and name == "loc.cur.":
                # Skip local currency if not displaying stocks.
                continue
            width = column["width"]
            output += f"{name:^{width}}"
        output += "\n"
        output += f"----------------------------------------------------------------------\n"

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
        index = 0
        name_col = row.name
        # Indent according to depth.
        for _ in range(0, row.depth):
            name_col = f"    {name_col}"

        width = self.columns[index]["width"]
        output += f"{name_col:<{width}}"

        # Set Allocation
        value = ""
        index = 1
        if row.set_allocation:
            value = f"{row.set_allocation:.2f}"
        width = self.columns[index]["width"]
        output += f"{value:>{width}}"

        # value
        index = 2
        value = f"{row.curr_value:,.0f}"
        width = self.columns[index]["width"]
        output += f"{value:>{width}}"

        # Value in security's currency. Show only if displaying full model, with stocks.
        if self.full:
            index = 3
            value = ""
            if row.curr_value_own_currency:
                value = f"({row.curr_value_own_currency:,.0f}"
                value += f" {row.own_currency}"
                value += ")"
            width = self.columns[index]["width"]
            output += f"{value:>{width}}"
        
        # Set value
        index = 4
        value = ""
        if row.set_value:
            value = f"{row.set_value:,.0f}"
        width = self.columns[index]["width"]
        output += f"{value:>{width}}"

        # https://en.wikipedia.org/wiki/ANSI_escape_code
        CSI="\x1B["
        # red = 31, green = 32
        # output += CSI+"31;40m" + "Colored Text" + CSI + "0m"

        # Value diff
        index = 5
        value = ""
        if row.diff_value:
            value = f"{row.diff_value:,.0f}"
            # Color the output
            # value = f"{CSI};40m{value}{CSI};40m"
        width = self.columns[index]["width"]
        output += f"{value:>{width}}"

        return output


class HtmlFormatter:
    """ Formats HTML output """
    pass
