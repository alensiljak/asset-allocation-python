""" Test configuration """
import pytest
from asset_allocation.config import Config

# @pytest.fixture(scope="session")
# def settings_db() -> Settings:
#     """ Settings for the real db file """
#     config_json = json.loads('{ "gnucash.database": "../data/test.gnucash" }')
#     config = Settings(config_json)
#     return config

# @pytest.fixture(scope="module")
# def svc(settings) -> BookAggregate:
#     """
#     Module-level book aggregate, using test settings, in-memory db. Read-only.
#     This is the default option as it is fast.
#     """
#     svc = BookAggregate(settings)
#     #create_test_data(svc)
#     return svc

@pytest.fixture(scope="session")
def aa_definition():
    ''' return the contents of the definition file '''
    definition = '''
    Allocation                                   100.00
    Allocation:Equity                             55.00
    Allocation:Fixed                              30.00
    Allocation:Fixed:Gov                          20.00
    Allocation:Fixed:Corp                         10.00
    Allocation:Real                               12.00
    Allocation:Cash                                3.00
    '''
    return definition

@pytest.fixture(scope="session")
def config():
    """ Test configuration """
    return Config("data/asset_allocation.ini")


class TestSettings(object):
    """
    Declares the settings and Book Aggregate as autouse.
    This means that individual tests do not need to mark the fixture explicitly.
    """
    def __init__(self):
        self.__config = config()

#     @pytest.fixture(autouse=True, scope="session")
#     def settings(self):
#         """ Returns the test settings json """
#         return settings()
#         # yield
#         # teardown

#     @pytest.fixture(autouse=True, scope="session")
#     def svc(self):
#         """ global Book Aggregate for all tests """
#         return svc(self.settings)

    @pytest.fixture(autouse=True, scope="session")
    def config(self):
        """ Real configuration """
        print("config???")
        return self.__config
