import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from app.main.adapters.orm import metadata, start_mappers
from app.test import config


@pytest.fixture
def postgres_engine():
    engine = create_engine(config.get_database_uri())
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session_factory(postgres_engine):
    yield sessionmaker(bind=postgres_engine)


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()
