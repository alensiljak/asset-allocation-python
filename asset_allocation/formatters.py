"""
Output formatters for the AA model
"""
from .model import AssetAllocationModel


class AsciiFormatter:
    """ Formats the model for the console output """
    # def __init__(self):
    #     super.__init__(self)

    def format(self, model: AssetAllocationModel):
        """ Returns the view-friendly output of the aa model """
        output = "AA model\n"
        output += "Total amount: " + str(model.total_amount) + "\n"
        # Asset classes
        output += "Asset Allocation\n"
        for ac in model.classes:
            output += str(ac) + "\n"
        return output

class HtmlFormatter:
    """ Formats HTML output """
    pass
    