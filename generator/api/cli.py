"""Flask CLI commands."""
import sys

import pytest
import click
from sqlalchemy import create_engine

from app.main.adapters import orm
from app.main import config as main_config
from app.test import config as test_config


@click.group()
def cli():
    pass


@cli.command("test")
@click.option("--verbose", "-v", is_flag=True)
@click.option("--unit/--no-unit", is_flag=True)
@click.option("--integration/--no-integration", is_flag=True)
@click.option("--e2e/--no-e2e", is_flag=True)
def run_tests(verbose, unit, integration, e2e):
    base = "app/test"
    options = ["-x"]
    # run unit tests
    if unit:
        options.append(f"{base}/unit")
    # run integration tests
    if integration:
        options.append(f"{base}/integration")
    # run end-to-end tests
    if e2e:
        options.append(f"{base}/e2e")
    # run all tests
    if options == ["-x"]:
        options.append(base)
    # verbose output
    if verbose:
        options.append("-v")
    result = pytest.main(options)
    if result == pytest.ExitCode.OK:
        return 0
    sys.exit(result.value)


@cli.command("create-tables")
@click.option("--test", "-t", is_flag=True)
def create_tables(test):
    uri = (
        test_config.get_database_uri()
        if test
        else main_config.get_database_uri()
    )
    engine = create_engine(uri)
    orm.metadata.create_all(engine)


@cli.command("drop-tables")
@click.option("--test", "-t", is_flag=True)
def dopr_tables(test):
    uri = (
        test_config.get_database_uri()
        if test
        else main_config.get_database_uri()
    )
    engine = create_engine(uri)
    orm.metadata.drop_all(engine)


if __name__ == "__main__":
    cli()
