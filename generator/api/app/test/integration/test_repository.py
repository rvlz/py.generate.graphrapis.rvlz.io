import pytest

from app.main.adapters import repository
from app.main.domain import model
from app.test import random_values


pytestmark = pytest.mark.usefixtures("mappers")


def generate_links(count: int, domain: str):
    links = []
    for i in range(count):
        links.append(
            model.Link(
                ref=random_values.generate_ref(),
                domain=domain,
                path=random_values.generate_path(),
                title=random_values.generate_title(),
            )
        )
    return links


def test_get_by_linkref(postgres_session_factory):
    session = postgres_session_factory()
    repo = repository.SqlAlchemyRepository(session)
    domain1, domain2 = (
        random_values.generate_domain(),
        random_values.generate_domain(),
    )
    link1, link2 = generate_links(2, domain1)
    (link3,) = generate_links(1, domain2)

    website1 = model.Website(domain1, links=[link1, link2])
    website2 = model.Website(domain2, links=[link3])
    repo.add(website1)
    repo.add(website2)

    assert repo.get_by_linkref(link1.ref) == website1
    assert repo.get_by_linkref(link3.ref) == website2
