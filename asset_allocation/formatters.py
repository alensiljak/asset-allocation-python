"""
Output formatters for the AA model
"""
from decimal import Decimal
from .model import AssetAllocationModel
from .maps import ModelMapper
from .view_model import AssetAllocationViewModel


class AsciiFormatter:
    """ Formats the model for the console output """

    def __init__(self):
        self.columns = [
            {"name": "Asset Class", "width": 22},
            {"name": "alloc.", "width": 5},
            {"name": "cur.al.", "width": 6},
            {"name": "diff.", "width": 6},
            {"name": "al.val.", "width": 8},
            {"name": "value", "width": 8},
            {"name": "loc.cur.", "width": 13},
            {"name": "diff", "width": 8}
        ]
        self.full = False

    def format(self, model: AssetAllocationModel, full: bool = False):
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
        output += f"-------------------------------------------------------------------------------\n"

        # Asset classes

        view_model = ModelMapper(model).map_to_linear(self.full)
        for row in view_model:
            output += self.__format_row(row) + "\n"

        return output

    def __format_row(self, row: AssetAllocationViewModel):
        """ display-format one row
        Formats one Asset Class record """
        output = ""
        index = 0

        # Name
        value = row.name
        # Indent according to depth.
        for _ in range(0, row.depth):
            value = f"   {value}"
        output += self.append_text_column(value, index)

        # Set Allocation
        value = ""
        index += 1
        if row.set_allocation > 0:
            value = f"{row.set_allocation:.2f}"
        output += self.append_num_column(value, index)

        # Current Allocation
        value = ""
        index += 1
        if row.curr_allocation > Decimal(0):
            value = f"{row.curr_allocation:.2f}"
        output += self.append_num_column(value, index)

        # Allocation difference, percentage
        value = ""
        index += 1
        # value = f"{row.diff_allocation:.2f}"
        if row.alloc_diff_perc > Decimal(0):
            value = f"{row.alloc_diff_perc:.0f} %"
        output += self.append_num_column(value, index)

        # Allocated value
        index += 1
        value = ""
        if row.set_value:
            value = f"{row.set_value:,.0f}"
        output += self.append_num_column(value, index)

        # Current Value
        index += 1
        value = f"{row.curr_value:,.0f}"
        output += self.append_num_column(value, index)

        # Value in security's currency. Show only if displaying full model, with stocks.
        index += 1
        if self.full:
            value = ""
            if row.curr_value_own_currency:
                value = f"({row.curr_value_own_currency:,.0f}"
                value += f" {row.own_currency}"
                value += ")"
            output += self.append_num_column(value, index)

        # https://en.wikipedia.org/wiki/ANSI_escape_code
        # CSI="\x1B["
        # red = 31, green = 32
        # output += CSI+"31;40m" + "Colored Text" + CSI + "0m"

        # Value diff
        index += 1
        value = ""
        if row.diff_value:
            value = f"{row.diff_value:,.0f}"
            # Color the output
            # value = f"{CSI};40m{value}{CSI};40m"
        output += self.append_num_column(value, index)

        return output

    def append_num_column(self, text: str, index: int):
        """ Add value to the output row, width based on index """
        width = self.columns[index]["width"]
        return f"{text:>{width}}"

    def append_text_column(self, text: str, index: int):
        """ Add value to the output row, width based on index """
        width = self.columns[index]["width"]
        return f"{text:<{width}}"


class HtmlFormatter:
    """ Formats HTML output """
    pass
