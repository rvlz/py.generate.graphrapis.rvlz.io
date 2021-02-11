import pytest
from sqlalchemy.orm import clear_mappers

from app.main import bootstrap, views
from app.main.domain import commands
from app.main.service_layer import unit_of_work
from app.test import random_values


@pytest.fixture
def postgres_bus(postgres_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(postgres_session_factory),
    )
    yield bus
    clear_mappers()


def test_link_views(postgres_bus):
    ref = random_values.generate_ref()
    postgres_bus.handle(
        commands.RegisterLink(
            ref=ref,
            domain="stackoverflow.com",
            path="kubernetes",
            title="Intro to Kubernetes",
        )
    )

    assert views.link(ref, postgres_bus.uow) == {
        "ref": ref,
        "domain": "stackoverflow.com",
        "path": "kubernetes",
        "title": "Intro to Kubernetes",
        "active": True,
    }


def test_latest_links_views(postgres_bus, capsys):
    links = [
        {
            "ref": random_values.generate_ref(),
            "domain": random_values.generate_domain(),
            "path": random_values.generate_path(),
            "title": random_values.generate_title(),
            "active": True,
        }
        for _ in range(4)
    ]
    for link in links:
        postgres_bus.handle(
            commands.RegisterLink(
                ref=link["ref"],
                domain=link["domain"],
                path=link["path"],
                title=link["title"],
            )
        )

    results = views.latest_links(2, postgres_bus.uow)
    assert len(results) == 2
    assert links[3] == results[0]
    assert links[2] == results[1]
