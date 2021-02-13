from app.main.domain import model, events
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


def test_get_link_doesnt_find_links_with_none_domain():
    domain = random_values.generate_domain()
    ref = random_values.generate_ref()
    link = model.Link(
        ref=ref,
        domain="stackoverflow.com",
        path="kubernetes",
        title="Intro to Kubernetes",
    )
    website = model.Website(domain=domain, links=[link])
    assert website.find(ref) == link
    link.domain = None
    assert website.find(ref) is None


def test_outputs_registration_event():
    domain = "stackoverflow.com"
    ref, other_ref = random_values.generate_ref(), random_values.generate_ref()
    path = "kubernetes"
    title = "Intro to Kubernetes"
    website = model.Website(domain=domain)
    link = model.Link(
        ref=ref,
        domain=domain,
        path=path,
        title=title,
        active=True,
    )
    other_link = model.Link(
        ref=other_ref,
        domain=domain,
        path=path,
        title=title,
        active=False,
    )
    website.register([link, other_link])
    expected_events = {
        events.LinkRegistered(
            ref=ref,
            domain=domain,
            path=path,
            title=title,
            active=True,
        ),
        events.LinkRegistered(
            ref=other_ref,
            domain=domain,
            path=path,
            title=title,
            active=False,
        ),
    }
    assert set(website.events[-2:]) == expected_events


def generate_link():
    ref = random_values.generate_ref()
    link = model.Link(
        ref=ref,
        domain=random_values.generate_path(),
        path=random_values.generate_path(),
        title=random_values.generate_title(),
        active=True,
    )
    return ref, link


def test_remove_registered_link():
    ref, link = generate_link()
    website = model.Website(domain=link.domain)
    website.register([link])
    assert website.find(ref) is not None
    website.remove(ref)
    assert website.find(ref) is None
