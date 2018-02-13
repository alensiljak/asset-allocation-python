"""
CLI for handling config files
"""
import click
from asset_allocation.config import Config

@click.group()
def config():
    """ Handles the config file """
    pass

@click.command()
def delete():
    """ Delete the current user's config file """
    cfg = Config()
    cfg.delete_user_config()

@click.command()
def show():
    """ Show the contents of the current config file """
    cfg = Config()
    # file_path = cfg.get_config_path()
    contents = cfg.get_contents()
    print(contents)

@click.command()
@click.option("--key", help="The name of the option to set.")
@click.option("--val", help="The name of the option to set.")
def set(key, val):
    """ Sets the values in the config file """
    if not key:
        print(f"Parameters --key and --val must be provided.")
        return

    cfg = Config()
    cfg.set(key, val)
    print(f"The {key} has been set to {val}.")

config.add_command(delete)
config.add_command(set)
config.add_command(show)
