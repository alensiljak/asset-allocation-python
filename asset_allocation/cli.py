"""
Main entry point to the library
"""
import sys
import click
from asset_allocation.config_cli import config
from asset_allocation.class_cli import ac
from asset_allocation import dal

@click.group()
def cli():
    pass

@click.command()
@click.option("--format", default="ascii", help="format for the report output. ascii or html.")
                # prompt="output format")
def show(format):
    """ Print current allocation to the console. """
    print(f"This would print the Asset Allocation report in **{format}** format. Incomplete.")


cli.add_command(ac)
cli.add_command(show)
cli.add_command(config)
