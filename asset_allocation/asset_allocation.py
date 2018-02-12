"""
Main entry point to the library
"""
import sys
import click

@click.group()
def cli():
    pass

def main():
    """ Run from the console """
    print("in main")
    show("html")

@click.command()
@click.option("--format", default="ascii", help="format for the report output. ascii or html.")
                # prompt="output format")
def show(format):
    """ Print current allocation to the console. """
    print(f"This would print the Asset Allocation report in {format} format. Incomplete.")

@click.command()
@click.option("--name", prompt="Asset Class name")
def add(name):
    """ Adds Asset Class """
    print("in add")


cli.add_command(show)
cli.add_command(add)

# if __name__ == '__main__':
#     main()
