"""
Main entry point to the library
"""
import sys
import click

@click.command()
@click.argument("command", default="default")
@click.option("--name")

def main(command, name):
    """ Run from the console """

    if command == "default":
        print("without any arguments, this should print out the current allocation report.")
    elif command == "add":
        print("add asset class")

def print_allocation():
    """ Print current allocation to the console. """
    print("allocation. Incomplete")

if __name__ == '__main__':
    main()
