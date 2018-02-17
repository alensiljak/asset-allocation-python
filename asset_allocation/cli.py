"""
Main entry point to the library
"""
import sys

import click

from asset_allocation import dal
from asset_allocation.app import AppAggregate
from asset_allocation.assetclass_cli import ac
from asset_allocation.config import Config
from asset_allocation.config_cli import config
from asset_allocation.formatters import AsciiFormatter, HtmlFormatter


@click.group()
def cli():
    pass

@click.command()
@click.option("--format", default="ascii", help="format for the report output. ascii or html.")
                # prompt="output format")
def show(format):
    """ Print current allocation to the console. """
    # load asset allocation
    app = AppAggregate()
    model = app.get_asset_allocation_model()

    if format == "ascii":
        formatter = AsciiFormatter()
    elif format == "html":
        formatter = HtmlFormatter
    else:
        raise ValueError(f"Unknown formatter {format}")
    output = formatter.format(model)
    print(output)
    print(f"This would print the Asset Allocation report in **{format}** format. Incomplete.")


cli.add_command(ac)
cli.add_command(show)
cli.add_command(config)

if __name__ == '__main__':
    show(["--format", "ascii"])
