""" Test the DAL """
from asset_allocation import dal
from asset_allocation.config import Config, ConfigKeys

def test_connect_to_db():
    """ Try to open database """
    cfg = Config()
    db_path = cfg.get(ConfigKeys.asset_allocation_database_path)

    session = dal.get_session(db_path)
    print(session)
