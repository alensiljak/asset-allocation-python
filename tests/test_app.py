"""
Test the main app functionality
"""
from asset_allocation.app import AppAggregate

#def test_asset_allocation_tree_generation():
    # """ Create an asset allocation tree """

def test_open_db():
    """ Open db connection from the app """
    app = AppAggregate()
    session = app.open_session()
    session.close()

    assert session != None
