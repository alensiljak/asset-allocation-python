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
@click.option("--name", prompt="Asset Class name", help="Name of the Asset Class")
def add(name):
    """ Add new Asset Class """
    print(f"Here we would add {name} and display its details.")
    print(f"Asset Class: {name}, Allocation...")

@click.command()
def test():
    """ Test functionality """
    pass


cli.add_command(show)
cli.add_command(add)
cli.add_command(config)
cli.add_command(test)

#test()