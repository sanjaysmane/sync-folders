#!/usr/bin/env python
import click
import time
from .syncfold import sync_folders

@click.command()
@click.argument('source_folder', required=1)
@click.argument('destination_folder', required=1)
@click.argument('name_of_logfile', required=1)
@click.argument('interval_mins', required=1)


def main(source_folder, destination_folder, name_of_logfile, interval_mins):
    sync_folders(source_folder, destination_folder, name_of_logfile)
    seconds = int(interval_mins)*60
    while seconds>60:
        sync_folders(source_folder, destination_folder, name_of_logfile)
        time.sleep(seconds)


if __name__ == "__main__":
    main()