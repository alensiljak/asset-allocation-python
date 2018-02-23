"""
Output formatters for the AA model
"""
from .model import AssetAllocationModel, AssetClass, Stock
from .maps import ModelMapper


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

        view_model = ModelMapper(model).map_to_linear(self.full)
        
        return output

    def __format_row(self):
        """ display-format one row """
        pass

class HtmlFormatter:
    """ Formats HTML output """
    pass
