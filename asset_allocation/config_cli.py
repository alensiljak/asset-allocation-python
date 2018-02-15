"""
CLI for handling config files
"""
import click
from asset_allocation.config import Config, ConfigKeys

@click.group()
def config():
    """ Operates the config file """
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
@click.option("--aadb", help="Asset Allocation database path. If only name used, it will be loaded from project's data directory.")
@click.option("--cur", help="Set the default currency symbol. (i.e. EUR, CHF)")
# @click.option("--key", help="The name of the option to set.")
# @click.option("--val", help="The name of the option to set.")
def set(aadb, cur):
    """ Sets the values in the config file """
    cfg = Config()
    edited = False

    if aadb:
        cfg.set(ConfigKeys.asset_allocation_database_path, aadb)
        print(f"The database has been set to {aadb}.")
        edited = True
    
    if cur:
        cfg.set(ConfigKeys.default_currency, cur)
        edited = True

    if edited:
        print(f"Changes saved.")
    else:
        print(f"No changes were made.")
        print(f"Use --help parameter for more information.")

@click.command()
@click.option("--aadb", is_flag=True, help="Displays the Asset Allocation database name/path.")
def get(aadb: str):
    """ Retrieves a value from config """
    if (aadb):
        cfg = Config()
        value = cfg.get(ConfigKeys.asset_allocation_database_path)
        click.echo(value)
    
    if not aadb:
        click.echo("Use --help for more information.")

config.add_command(delete)
config.add_command(get)
config.add_command(set)
config.add_command(show)
