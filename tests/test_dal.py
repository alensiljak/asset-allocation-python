""" Test the DAL """
from asset_allocation import dal

def test_connect_to_db():
    """ Try to open database """
    session = dal.session
    print(session)
