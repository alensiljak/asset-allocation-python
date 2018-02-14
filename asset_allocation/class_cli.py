"""
CLI for dealing with Asset Classes
"""
import click
from decimal import Decimal
from asset_allocation.app import AppAggregate
from asset_allocation.dal import AssetClass

@click.group()
def ac():
    """ Operates the Asset Class records """
    pass

@click.command()
@click.argument("name", "-n") #, prompt="Asset Class name") # help="Name of the Asset Class"
def add(name):
    """ Add new Asset Class """
    item = AssetClass()
    item.name = name
    app = AppAggregate()
    app.create_asset_class(item)
    
    print(f"Asset class {name} created.")

@click.command()
@click.argument("id", type=int)
def delete(id):
    """ Deletes asset class record """
    app = AppAggregate()
    app.delete(id)

@click.command()
@click.argument("id", type=int)
@click.option("--parent", "-p", type=int, help="Set the parent")
@click.option("--alloc", "-a", type=Decimal)
def edit(id: int, parent: int, alloc: Decimal):
    """ Edit asset class """
    saved = False

    # load
    app = AppAggregate()
    item = app.get(id)
    if not item:
        raise KeyError("Asset Class with id %s not found.", id)
    
    if parent:
        assert parent != id, "Parent can not be set to self."

        # TODO check if parent exists?

        item.parentid = parent
        saved = True
        # click.echo(f"parent set to {parent}")
    
    if alloc:
        assert alloc != Decimal(0)

        item.allocation = alloc
        saved = True

    app.save()
    if saved:
        click.echo("Data saved.")
    else:
        click.echo("No data modified. Use --help to see possible parameters.")

@click.command()
def list():
    """ Lists all asset classes """
    session = AppAggregate().open_session()
    classes = session.query(AssetClass).all()
    print(classes)


ac.add_command(add)
ac.add_command(delete)
ac.add_command(edit)
ac.add_command(list)
