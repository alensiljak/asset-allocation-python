"""
Main entry point to the library
"""
import sys
import click
from asset_allocation.config_cli import config
#from .dal import AssetClass
from asset_allocation import dal
from asset_allocation.app import AppAggregate

@click.group()
def cli():
    pass

@click.command()
@click.option("--format", default="ascii", help="format for the report output. ascii or html.")
                # prompt="output format")
def show(format):
    """ Print current allocation to the console. """
    print(f"This would print the Asset Allocation report in **{format}** format. Incomplete.")

@click.command()
@click.option("--name", "-n", prompt="Asset Class name", help="Name of the Asset Class")
def add(name):
    """ Add new Asset Class """
    item = dal.AssetClass()
    item.name = name
    app = AppAggregate()
    app.create_asset_class(item)
    
    print(f"Asset class {name} created.")

@click.command()
@click.argument("id", type=int)
@click.option("--parent", type=int, help="Set the parent")
def edit(id: int, parent: int):
    """ Edit asset class """
    saved = False

    # load
    app = AppAggregate()
    item = app.get(id)
    if not item:
        raise KeyError("Asset Class with id %s not found.", id)
    
    if (parent):
        item.parent = parent
        saved = True
        click.echo(f"parent set to {parent}")
    
    app.save()
    if saved:
        click.echo("Data saved.")
    else:
        click.echo("No data modified. Use --help to see possible parameters.")

@click.command()
def list():
    """ Lists all asset classes """
    session = dal.get_session()
    classes = session.query(dal.AssetClass).all()
    print(classes)


cli.add_command(show)
cli.add_command(add)
cli.add_command(config)
cli.add_command(edit)
cli.add_command(list)
