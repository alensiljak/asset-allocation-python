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
    file_path = cfg.get_config_path()
    contents = cfg.get_contents(file_path)
    print(contents)

config.add_command(delete)
config.add_command(show)
