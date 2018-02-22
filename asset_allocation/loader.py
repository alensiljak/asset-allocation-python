""" Asset Allocation loader """
from decimal import Decimal
from logging import DEBUG, log
from typing import List

from gnucash_portfolio.bookaggregate import BookAggregate
from piecash import Account, Book, Commodity, open_book
from pricedb.model import PriceModel

from . import dal
from .config import Config, ConfigKeys
from .maps import AssetClassMapper
from .model import AssetAllocationModel, AssetClass, Stock
from .stocks import StocksInfo


class AssetAllocationLoader:
    """ The new allocation loader """
    def __init__(self, config=None, session=None):
        self.session = session
        self.config = config
        self.mapper = None
        self.model: AssetAllocationModel = None

    def load_cash_balances(self):
        """ Loads cash balances from GnuCash book and recalculates into the default currency """
        from gnucash_portfolio.accounts import AccountsAggregate, AccountAggregate
        from gnucash_portfolio.currencies import CurrenciesAggregate

        cfg = self.__get_config()
        cash_root_name = cfg.get(ConfigKeys.cash_root)
        # Load cash from all accounts under the root.
        gc_db = self.config.get(ConfigKeys.gnucash_book_path)
        with open_book(gc_db) as book:
            # currency
            cur_agg = CurrenciesAggregate(book)
            currency = cur_agg.get_by_symbol(self.model.currency)

            svc = AccountsAggregate(book)
            root_account = svc.get_by_fullname(cash_root_name)
            acct_svc = AccountAggregate(book, root_account)
            cash_balance = acct_svc.get_cash_balance_with_children(root_account, currency)
            #book.flush()

        # assign to cash asset class.
        cash = self.model.get_cash_asset_class()
        cash.curr_value = cash_balance

    def load_tree_from_db(self) -> AssetAllocationModel:
        """ Reads the asset allocation data only, and constructs the AA tree """
        self.model = AssetAllocationModel()

        # currency
        self.model.currency = self.__get_config().get(ConfigKeys.default_currency)

        # Asset Classes
        db = self.__get_session()
        first_level = (
            db.query(dal.AssetClass)
            .filter(dal.AssetClass.parentid == None)
            .order_by(dal.AssetClass.sortorder)
            .all()
        )

        # create tree
        for entity in first_level:
            ac = self.__map_entity(entity)
            self.model.classes.append(ac)
            # Add to index
            self.model.asset_classes.append(ac)

            # append child classes recursively
            self.__load_child_classes(ac)

        return self.model

    def load_stock_links(self):
        """ Read stock links into the model """
        links = self.__get_session().query(dal.AssetClassStock).all()
        for entity in links:
            # log(DEBUG, f"adding {entity.symbol} to {entity.assetclassid}")
            # mapping
            stock: Stock = Stock(entity.symbol)
            # find parent classes by id and assign children
            parent: AssetClass = self.model.get_class_by_id(entity.assetclassid)
            if parent:
                # Assign to parent.
                parent.stocks.append(stock)
                # Add to index for easy reference
                self.model.stocks.append(stock)

    def load_stock_quantity(self):
        """ Loads quantities for all stocks """
        info = StocksInfo(self.config)
        for stock in self.model.stocks:
            stock.quantity = info.load_stock_quantity(stock.symbol)
        info.gc_book.close()

    def load_stock_prices(self):
        """ Load latest prices for securities """
        info = StocksInfo(self.config)
        for stock in self.model.stocks:
            price: PriceModel = info.load_latest_price(stock.symbol)
            if not price:
                price = PriceModel()
                price.currency = self.config.get(ConfigKeys.default_currency)
            stock.price = price.value
            stock.currency = price.currency
        info.close_databases()

    def recalculate_stock_values_into_base(self):
        """ Loads the exchange rates and recalculates stock holding values into 
        base currency """
        with BookAggregate() as svc:
            for stock in self.model.stocks:
                val_base = svc.currencies.get_amount_in_base_currency(stock.currency, stock.value)
                stock.value_in_base_currency = val_base

    def __load_child_classes(self, ac: AssetClass):
        """ Loads child classes/stocks """
        # load child classes for ac
        db = self.__get_session()
        entities = (
            db.query(dal.AssetClass)
            .filter(dal.AssetClass.parentid == ac.id)
            .order_by(dal.AssetClass.sortorder)
            .all()
        )
        # map
        for entity in entities:
            child_ac = self.__map_entity(entity)
            # depth
            child_ac.depth = ac.depth + 1
            ac.classes.append(child_ac)
            # Add to index
            self.model.asset_classes.append(child_ac)

            self.__load_child_classes(child_ac)

    def __map_entity(self, entity: dal.AssetClass) -> AssetClass:
        """ maps the entity onto the model object """
        mapper = self.__get_mapper()
        ac = mapper.map_entity(entity)
        return ac

    def __get_mapper(self):
        """ mapper instance """
        if self.mapper == None:
            self.mapper = AssetClassMapper()
        return self.mapper

    def __get_session(self):
        """ Opens a db session """
        db_path = self.__get_config().get(ConfigKeys.asset_allocation_database_path)
        self.session = dal.get_session(db_path)
        return self.session

    def __get_config(self):
        """ returns/creates a config object """
        if not self.config:
            self.config = Config()
        return self.config

    def __load_asset_class(self, ac_id: int):
        """ Loads Asset Class entity """
        # open database
        db = self.__get_session()
        entity = db.query(dal.AssetClass).filter(dal.AssetClass.id == ac_id).first()
        return entity


class _AllocationLoader:
    """ Parses the allocation settings and loads the current allocation from database """
    def __init__(self, currency: Commodity, book: Book):
        self.currency = currency
        self.book = book
        self.asset_allocation = None
        # Asset Class index populated during load, for performance.
        self.asset_class_index = {}

    # def load_asset_allocation_model(self):
    #     """ Loads Asset Allocation model for display """
    #     self.asset_allocation = self.load_asset_allocation_config()
    #     # Populate values from database.
    #     self.__load_values_into(self.asset_allocation)

    #     # calculate percentages
    #     total_value = self.asset_allocation.curr_value
    #     self.__calculate_percentages(self.asset_allocation, total_value)

    #     # Return model.
    #     model = {
    #         'allocation': self.asset_allocation,
    #         'currency': self.currency.mnemonic
    #     }

    #     return model

    # def load_asset_allocation_config(self) -> AssetGroup:
    #     """ Loads only the configuration from json """
    #             # read asset allocation file
    #     root_node = self.__load_asset_allocation_config_json()
    #     result = self.__parse_node(root_node)
    #     return result

    # def __load_values_into(self, asset_group: AssetGroup):
    #     """
    #     Populates the asset class values from the database.
    #     Reads the stock values and fills the asset classes.
    #     """
    #     # iterate recursively until an Asset Class is found.
    #     for child in asset_group.classes:
    #         if isinstance(child, AssetGroup):
    #             self.__load_values_into(child)

    #         if isinstance(child, AssetClass):
    #             # Add all the stock values.
    #             svc = SecuritiesAggregate(self.book)
    #             for stock in child.stocks:
    #                 # then, for each stock, calculate value
    #                 symbol = stock.symbol
    #                 cdty = svc.get_stock(symbol)
    #                 stock_svc = SecurityAggregate(self.book, cdty)

    #                 # Quantity
    #                 quantity = stock_svc.get_quantity()
    #                 stock.quantity = quantity

    #                 # last price
    #                 last_price: Price = stock_svc.get_last_available_price()
    #                 stock.price = last_price.value

    #                 # Value
    #                 stock_value = last_price.value * quantity
    #                 if last_price.currency != self.currency:
    #                     # Recalculate into the base currency.
    #                     stock_value = self.get_value_in_base_currency(
    #                         stock_value, last_price.currency)

    #                 child.curr_value += stock_value

    #         if child.name == "Cash":
    #             # load cash balances
    #             child.curr_value = self.get_cash_balance(child.root_account)

    #         asset_group.curr_value += child.curr_value

    # def get_value_in_base_currency(self, value: Decimal, currency: Commodity) -> Decimal:
    #     """ Recalculates the given value into base currency """
    #     base_cur = self.currency

    #     svc = CurrencyAggregate(self.book, currency)
    #     last_price = svc.get_latest_rate(base_cur)

    #     result = value * last_price.value

    #     return result

    # def get_cash_balance(self, root_account_name: str) -> Decimal:
    #     """ Loads investment cash balance in base currency """
    #     svc = AccountsAggregate(self.book)
    #     root_account = svc.get_by_fullname(root_account_name)
    #     acct_svc = AccountAggregate(self.book, root_account)
    #     result = acct_svc.get_cash_balance_with_children(root_account, self.currency)
    #     return result

    # def __parse_node(self, node):
    #     """Creates an appropriate entity for the node. Recursive."""
    #     entity = None

    #     if "classes" in node:
    #         # Asset Class Group
    #         entity = AssetGroup(node)
    #         child_allocation_sum = Decimal(0)
    #         # Process child nodes
    #         for child_node in node["classes"]:
    #             # recursive call
    #             child = self.__parse_node(child_node)

    #             child.parent = entity
    #             # log(DEBUG, "adding %s as parent to %s", entity.name, child.name)
    #             entity.classes.append(child)
    #             child_allocation_sum += child.allocation

    #         # compare allocation to the sum of child allocations
    #         if entity.allocation != child_allocation_sum:
    #             raise ValueError("allocation does not match (self/child)",
    #                              entity.allocation, child_allocation_sum)

    #     if "stocks" in node:
    #         # Asset Class
    #         entity = AssetClass(node)

    #     # Cash
    #     if node["name"] == "Cash":
    #         # Cash node
    #         entity = AssetClass(node)
    #         entity.root_account = node["rootAccount"]

    #     # Threshold
    #     if "threshold" in node:
    #         threshold = node["threshold"].replace('%', '')
    #         entity.threshold = Decimal(threshold)

    #     # add asset class to index.
    #     self.asset_class_index[entity.name] = entity
    #     # log(DEBUG, "adding %s (%s) to asset class index", entity.name, entity.fullname)
    #     # log(DEBUG, "%s", self.asset_class_index)

    #     return entity

    # def __load_asset_allocation_config_json(self):
    #     """
    #     Loads asset allocation from the file.
    #     Returns the list of asset classes.
    #     """
    #     allocation_file = path.abspath(path.join(
    #         os.path.dirname(os.path.realpath(__file__)), "../config/assetAllocation.json"))
    #     with open(allocation_file, 'r') as json_file:
    #         allocation_json = json.load(json_file)
    #     return allocation_json

    # def __calculate_percentages(self, asset_group: AssetGroup, total: Decimal):
    #     """ calculate the allocation percentages """
    #     if not hasattr(asset_group, "classes"):
    #         return

    #     for child in asset_group.classes:
    #         # calculate
    #         # allocation is read from the config.
    #         child.curr_alloc = child.curr_value * 100 / total
    #         child.alloc_diff = child.curr_alloc - child.allocation
    #         child.alloc_diff_perc = child.alloc_diff * 100 / child.allocation

    #         # Values
    #         child.alloc_value = total * child.allocation / 100
    #         # Value is calculated during load.
    #         #child.curr_value = total * child.curr_alloc / 100
    #         child.value_diff = child.curr_value - child.alloc_value

    #         # Threshold
    #         child.over_threshold = abs(child.alloc_diff_perc) > self.asset_allocation.threshold

    #         self.__calculate_percentages(child, total)
    #     return


class AssetAllocationAggregate():
    """
    The main service class.
    Opens a database connection when needed.
    """
    def __init__(self, config: Config):
        # book: Book
        self.book = None
        # self.root: AssetGroup = None
        # index for asset classes
        self.__asset_class_index = None
        # index for stocks
        self.__stock_index: List[Stock] = None

    # def load_full_model(self, currency: Commodity):
    #     """ Populates complete Asset Allocation tree """
    #     loader = _AllocationLoader(currency, self.book)
    #     return loader.load_asset_allocation_model()

    # def load_config_only(self, currency: Commodity):
    #     """ Loads only the asset allocation tree from configuration """
    #     loader = _AllocationLoader(currency, self.book)
    #     config = loader.load_asset_allocation_config()
    #     # get the asset class index
    #     self.__asset_class_index = loader.asset_class_index
    #     return config

    # def find_class_by_fullname(self, fullname: str):
    #     """ Locates the asset class by fullname. i.e. Equity:International """
    #     found = self.__get_by_fullname(self.root, fullname)
    #     return found

    def __get_by_fullname(self, asset_class, fullname: str):
        """ Recursive function """
        if asset_class.fullname == fullname:
            return asset_class

        if not hasattr(asset_class, "classes"):
            return None

        for child in asset_class.classes:
            found = self.__get_by_fullname(child, fullname)
            if found:
                return found

        return None

    # def get_stock(self, symbol: str) -> List[Stock]:
    #     """ Finds all the stock allocations by symbol """
    #     # find this symbol
    #     instances = [self.stock_index[symbol] for index_symbol in self.stock_index if index_symbol == symbol]
    #     # log(DEBUG, "found %s instances for symbol %s", instances, symbol)
    #     return instances

    # @property
    # def stock_index(self):
    #     """ Creates index of all stock symbols in allocation """
    #     # iterate through allocation, get all the stocks, put them into index
    #     if self.__stock_index:
    #         return self.__stock_index
    #     index = {}

    #     # log(DEBUG, "starting with asset class index %s", self.asset_class_index)
    #     # create asset class index first.
    #     for name in self.asset_class_index:
    #         asset_class = self.asset_class_index[name]
    #         # log(DEBUG, "%s found in asset class index. Parent: %s",
    #         #     asset_class.name, asset_class.parent)

    #         if isinstance(asset_class, AssetGroup):
    #             continue
    #         # if not isinstance(asset_class, AssetClass):
    #         for stock in asset_class.stocks:
    #             symbol = stock.symbol
    #             # populate
    #             index[symbol] = stock
    #             # log(DEBUG, "adding %s to stock index", symbol)

    #     # log(DEBUG, "stock index complete: %s", index)
    #     self.__stock_index = index
    #     return self.__stock_index
