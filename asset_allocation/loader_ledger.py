'''
Loader for ledger-style files.
'''
from decimal import Decimal
from .model import AssetAllocationModel, AssetClass, Stock, CashBalance


class AssetAllocationLoaderLedger:
    ''' Loader for ledger-style files. '''

    def __init__(self):
        # self.model = None
        pass

    def load_dictionary(self, definition: str):
        ''' load aa definition into a key/value index '''
        index = {}
        aa_root = None

        lines = self.__get_lines(definition)

        # parse lines, load tree
        for line in lines:
            parts = line.split()
            fullname = parts[0]
            value = parts[1]

            asset_class = {}
            asset_class['fullname'] = fullname
            asset_class['allocation'] = Decimal(value)

            if ':' in fullname:
                # non-root
                lastSeparatorIndex = fullname.rfind(':')
                asset_class['name'] = fullname[lastSeparatorIndex+1:]

                # find parent
                parent_fullname = fullname[:lastSeparatorIndex]
                parent = index.get(parent_fullname)
                if not 'children' in parent:
                    parent['children'] = []
                parent['children'].append(asset_class)
            else:
                # root class
                asset_class['name'] = fullname
                aa_root = asset_class

            # maintain index: name/value pair
            index[fullname] = asset_class

            #model.list.append({ 'fullname': name, 'asset_class': asset_class})
            #aa_root[fullname] = asset_class

        return aa_root

    def load_definition(self, definition: str = None):
        ''' load aa definition from a file '''
        model = AssetAllocationModel()

        # if definition passed, use it.
        if definition is None:
            definition = self.read_file()

        lines = self.__get_lines(definition)
        # parse lines, load tree
        for line in lines:
            parts = line.split()
            name = parts[0]
            value = parts[1]

            asset_class = AssetClass()
            asset_class.allocation = Decimal(value)

            if ':' in name:
                # non-root
                lastSeparatorIndex = name.rfind(':')
                asset_class.name = name[lastSeparatorIndex+1:]
                parent_fullname = name[:lastSeparatorIndex]

                # find parent
                parents = [x for x in model.list if x.get('fullname') == parent_fullname]
                assert len(parents) == 1
                parent = parents[0]
                parent_obj: AssetClass = parent.get('asset_class')
                parent_obj.classes.append(asset_class)
            else:
                # root class
                asset_class.name = name

            # maintain index: name/value pair
            model.list.append({'fullname': name, 'asset_class': asset_class})

        return model

    def read_file(self):
        ''' read the allocation contents '''
        content = ""
        # todo read file
        return content

    def __get_lines(self, definition):
        ''' prepare raw text lines for use '''
        src_lines = definition.splitlines()
        dest_lines = []

        for line in src_lines:
            if not line:
                continue

            line = line.strip()
            if not line:
                continue

            dest_lines.append(line)

        return dest_lines
