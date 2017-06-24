# -*- coding: utf-8 -*-

"""Console script for inaugurate."""

import os
import pprint
import sys

import click

from . import __version__ as VERSION
from .inaugurate import Inaugurate, InaugurateConfig, InaugurateException


@click.command()
@click.option('--version', help='the version of inaugurate you are running', is_flag=True)
@click.argument('ingrate', required=True, nargs=1)
def cli(version, ingrate):
    """Console script for inaugurate."""

    if version:
        click.echo(VERSION)
        sys.exit(0)

    try:
        inaugurate = Inaugurate(ingrate)
        inaugurate.inaugurate.run(os.path.expanduser("~/.inaugurate/runs/"), force=True, ansible_verbose="", callback="nsbl_internal")

    except (InaugurateException) as e:
        click.echo(e, err=True)
        sys.exit(1)

if __name__ == "__main__":
    cli()
