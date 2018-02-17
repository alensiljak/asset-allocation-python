"""
Output formatters for the AA model
"""
from .model import AssetAllocationModel, AssetClass


class AsciiFormatter:
    """ Formats the model for the console output """
    def __init__(self):
        self.columns = [("Asset Class", 25), ("allocation", 5)]

    def format(self, model: AssetAllocationModel):
        """ Returns the view-friendly output of the aa model """
        # Header
        output = f"Asset Allocation model, total: {model.currency} {str(model.total_amount)}\n"
        # Columns
        width = self.columns[0][1]
        output += f"{self.columns[0][0]:^{width}}"
        output += f"{self.columns[1][0]:^{self.columns[1][1]}}"
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
        return output

    def __get_ac_row(self, ac: AssetClass):
        """ Formats one Asset Class record """
        output = ""
        # Indent according to depth.
        for _ in range(0, ac.depth):
            output = f"    {output}"
        
        width = self.columns[0][1]
        output += f"{ac.name:<{width}}: "
        
        allocation = f"{ac.allocation:.2f}"
        output += f"{allocation:>5}"

        # https://en.wikipedia.org/wiki/ANSI_escape_code
        # CSI="\x1B["
        # # red = 31, green = 32
        # output += CSI+"31;40m" + "Colored Text" + CSI + "0m"
        
        return output

class HtmlFormatter:
    """ Formats HTML output """
    pass
    