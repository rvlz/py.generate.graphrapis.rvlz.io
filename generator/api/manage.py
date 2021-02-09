"""Flask CLI commands."""
from flask.cli import FlaskGroup

from app.main.entrypoints.flask_app import generate_app_factory
from app.main import bootstrap

cli = FlaskGroup(create_app=generate_app_factory(bus=bootstrap.bootstrap()))

if __name__ == "__main__":
    cli()
