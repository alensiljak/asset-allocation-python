"""
Test Asset Allocation loading and parsing
"""
from logging import log, DEBUG
from os import path
from asset_allocation.config import Config, ConfigKeys
from asset_allocation.loader import AssetAllocationLoader
from asset_allocation.model import AssetAllocationModel

def test_creation():
    """ Load correct types and something returned """
    x = AssetAllocationLoader()
    actual = x.load_tree_from_db()

    assert actual != None
    assert isinstance(actual, AssetAllocationModel)

def test_loading_records(config: Config):
    """ Load test data from db """
    db_path = config.get(ConfigKeys.asset_allocation_database_path)
    full_path = path.abspath(db_path)
    log(DEBUG, f"db: {db_path}, {full_path}")

    x: AssetAllocationLoader = AssetAllocationLoader(config=config)
    # log(DEBUG, f"using configuration: {x.config}")
    actual = x.load_tree_from_db()

    assert len(actual.classes) == 2
