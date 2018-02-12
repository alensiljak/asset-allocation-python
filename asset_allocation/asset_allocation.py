"""
Main entry point to the library
"""
import sys
import click

@click.group()
def cli():
    pass

@click.command()
@click.option("--format", default="ascii", help="format for the report output. ascii or html.")
                # prompt="output format")
def list(format):
    """ Print current allocation to the console. """
    print(f"This would print the Asset Allocation report in **{format}** format. Incomplete.")

@click.command()
@click.option("--name", prompt="Asset Class name", help="Name of the Asset Class")
def add(name):
    """ Add new Asset Class """
    print(f"Here we would add {name}.")


cli.add_command(list)
cli.add_command(add)
