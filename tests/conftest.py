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


class TestSettings(object):
    """
    Declares the settings and Book Aggregate as autouse.
    This means that individual tests do not need to mark the fixture explicitly.
    """
    def __init__(self):
        self.__config = Config()

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
        return self.__config
