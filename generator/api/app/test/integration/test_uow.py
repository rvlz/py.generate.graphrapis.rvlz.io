import pytest

from app.main.service_layer import unit_of_work, errors
from app.main.domain import model
from app.test import random_values


pytestmark = pytest.mark.usefixtures("mappers")


def test_uow_rolls_back_uncommitted_work_by_default(postgres_session_factory):
    ref = random_values.generate_ref()
    domain = random_values.generate_domain()
    uow = unit_of_work.SqlAlchemyUnitOfWork(postgres_session_factory)
    with uow:
        uow.session.execute(
            "INSERT INTO website (domain) VALUES (:domain)",
            dict(domain=domain),
        )
        uow.session.execute(
            "INSERT INTO link (ref, domain, path, title) VALUES "
            "(:ref, :domain, :path, :title)",
            dict(
                ref=ref,
                domain=domain,
                path="kubernetes",
                title="Intro to Kubernetes",
            ),
        )
    new_session = postgres_session_factory()
    rows = list(
        new_session.execute(
            "SELECT * FROM link WHERE ref=:ref",
            dict(ref=ref),
        )
    )
    assert rows == []


def test_uow_raises_exception_for_duplicate_fields(postgres_session_factory):
    session = postgres_session_factory()
    ref = random_values.generate_ref()
    domain = random_values.generate_domain()
    session.execute(
        "INSERT INTO website (domain) VALUES (:domain)",
        dict(domain=domain),
    )
    session.execute(
        "INSERT INTO link (ref, domain, path, title) VALUES "
        "(:ref, :domain, :path, :title)",
        dict(
            ref=ref,
            domain=domain,
            path="kubernetes",
            title="Intro to Kubernetes",
        ),
    )
    session.commit()
    session.close()

    uow = unit_of_work.SqlAlchemyUnitOfWork(postgres_session_factory)
    with pytest.raises(errors.DuplicateFieldError) as exc:
        with uow:
            website = uow.websites.get(domain)
            website.links.append(
                model.Link(
                    ref=ref,
                    domain=domain,
                    path="docker",
                    title="Intro to Docker",
                )
            )
            uow.commit()
    assert exc.value.resource == "link"
    assert exc.value.field == "ref"
    assert exc.value.value == ref
