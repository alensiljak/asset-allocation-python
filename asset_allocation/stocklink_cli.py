""" CLI for handling stock links """
import logging
import sys

import click
import click_log

from .app import AppAggregate

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
def sl():
    """ Stock link handling """
    pass

@click.command("import")
@click.argument("file")
def import_csv(file):
    """ Import stock links from a .csv file """
    lines = ""
    with open(file) as csv_file:
        lines = csv_file.readlines()

    # Header, the first line.    
    header = lines[0]
    lines.remove(header)
    header = header.rstrip()

    # Parse records from a csv row.
    counter = 0
    app = AppAggregate()
    app.open_session()
    for line in lines:
        # Create insert statements
        line = line.rstrip()
        command = f"insert into AssetClass_Stock ({header}) values ({line});"
        # insert records
        app.session.execute(command)
        try:
            app.save()
        except:
            print(f"error: ", sys.exc_info()[0])
            app.session.close()
        counter += 1
    print(f"Data imported. {counter} rows created.")

    return False

@click.command("export")
def export_symbols():
    """ Exports all the symbols used in asset allocation """
    app = AppAggregate()
    app.export_symbols()

@click.command()
@click_log.simple_verbosity_option(logger)
def unallocated():
    """ Identify unallocated holdings """
    app = AppAggregate()
    app.logger = logger
    unalloc = app.find_unallocated_holdings()

    for item in unalloc:
        print(item)


#############################
sl.add_command(import_csv)
sl.add_command(export_symbols)
sl.add_command(unallocated)
