from app.main.domain import model
from app.test import random_values


def test_link_is_registered(capsys):
    domain = random_values.generate_domain()
    ref = random_values.generate_ref()
    website = model.Website(domain=domain)
    link = model.Link(
        ref=ref,
        domain=domain,
        path="kubernetes",
        title="Intro to Kubernetes",
    )
    assert not website.registered(link)
    website.register([link])
    assert website.registered(link)


def test_can_only_register_links_with_same_domain():
    domain, other_domain = (
        random_values.generate_domain(),
        random_values.generate_domain(),
    )
    ref, other_ref = random_values.generate_ref(), random_values.generate_ref()
    website = model.Website(domain=domain)
    link = model.Link(
        ref=ref,
        domain=domain,
        path="kubernetes",
        title="Intro to Kubernetes",
    )
    other_link = model.Link(
        ref=other_ref,
        domain=other_domain,
        path="kubernetes",
        title="Kubernetes",
    )
    assert website.can_register(link)
    assert not website.can_register(other_link)


def test_get_link_by_ref():
    domain = random_values.generate_domain()
    ref, other_ref = random_values.generate_ref(), random_values.generate_ref()
    link = model.Link(
        ref=ref,
        domain=domain,
        path="kubernetes",
        title="Intro to Kubernetes",
    )
    other_link = model.Link(
        ref=other_ref,
        domain=domain,
        path="kubernetes",
        title="Kubernetes",
    )
    website = model.Website(domain=domain, links=[link, other_link])
    assert website.find(link.ref) == link
