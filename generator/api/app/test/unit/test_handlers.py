from app.main import bootstrap
from app.main.adapters import repository
from app.main.service_layer import unit_of_work
from app.main.domain import model, commands
from app.test import random_values


class FakeRepository(repository.AbstractRepository):
    def __init__(self):
        super().__init__()
        self.websites = set()

    def _add(self, website: model.Website):
        self.websites.add(website)

    def _get(self, domain: str) -> model.Website:
        return next((w for w in self.websites if w.domain == domain), None)

    def _get_by_linkref(self, linkref: str) -> model.Website:
        return next(
            (
                website
                for website in self.websites
                for link in website.links
                if link.ref == linkref
            ),
            None,
        )


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.committed = False
        self.websites = FakeRepository()

    def __enter__(self):
        return super().__enter__()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def message_bus():
    return bootstrap.bootstrap(start_orm=False, uow=FakeUnitOfWork())


class TestRegisterLinks:
    def test_for_new_website(self):
        bus = message_bus()
        bus.handle(
            commands.RegisterLink(
                ref="ln",
                domain="stackoverflow.com",
                path="kubernetes",
                title="Intro to Kubernetes",
                active=True,
            )
        )
        assert bus.uow.websites.get("stackoverflow.com") is not None
        assert bus.uow.committed

    def test_for_existing_website(self):
        bus = message_bus()
        bus.handle(
            commands.RegisterLink(
                ref="ln",
                domain="stackoverflow.com",
                path="kubernetes",
                title="Intro to Kubernetes",
                active=True,
            )
        )
        bus.handle(
            commands.RegisterLink(
                ref="ln1",
                domain="stackoverflow.com",
                path="docker",
                title="Intro to Docker",
                active=True,
            )
        )
        assert (
            bus.uow.websites.get("stackoverflow.com").find("ln1") is not None
        )

    def test_register_link(self):
        bus = message_bus()
        bus.handle(
            commands.RegisterLink(
                ref="ln",
                domain="stackoverflow.com",
                path="kubernetes",
                title="Intro to Kubernetes",
                active=True,
            )
        )
        assert bus.uow.websites.get("stackoverflow.com").find("ln") is not None

    def test_bulk_register_links(self):
        bus = message_bus()
        bus.handle(
            commands.BulkRegisterLinks(
                links=[
                    {
                        "ref": "ln",
                        "domain": "stackoverflow.com",
                        "path": "kubernetes",
                        "title": "Intro to Kubernetes",
                        "active": True,
                    },
                    {
                        "ref": "ln1",
                        "domain": "wikipedia.org",
                        "path": "docker",
                        "title": "Docker",
                        "active": True,
                    },
                ]
            )
        )
        assert bus.uow.websites.get("stackoverflow.com").find("ln") is not None
        assert bus.uow.websites.get("wikipedia.org").find("ln1") is not None
        assert bus.uow.committed


class TestDeregisterLink:
    def test_deregister_link(self):
        bus = message_bus()
        bus.handle(
            commands.RegisterLink(
                ref="ln",
                domain="stackoverflow.com",
                path="kubernetes",
                title="Intro to Kubernetes",
                active=True,
            )
        )
        link = bus.uow.websites.get("stackoverflow.com").find("ln")
        assert link.active
        bus.uow.committed = False
        bus.handle(commands.DeregisterLink(ref="ln"))
        assert not link.active
        assert bus.uow.committed


class TestLinkUpdate:
    def test_update_all_attr_with_no_domain_change(self):
        ref = random_values.generate_ref()
        bus = message_bus()
        bus.handle(
            commands.RegisterLink(
                ref=ref,
                domain="stackoverflow.com",
                path="kubernetes",
                title="Intro to Kubernetes",
                active=True,
            )
        )
        assert bus.uow.websites.get("stackoverflow.com").find(ref) is not None
        bus.handle(
            commands.UpdateLink(
                ref=ref,
                domain=None,
                path="docker",
                title="Docker",
                active=False,
            )
        )
        link = bus.uow.websites.get("stackoverflow.com").find(ref)
        assert link is not None
        assert link.ref == ref
        assert link.domain == "stackoverflow.com"
        assert link.path == "docker"
        assert link.title == "Docker"
        assert not link.active

    def test_update_only_domain(self):
        ref = random_values.generate_ref()
        bus = message_bus()
        bus.handle(
            commands.RegisterLink(
                ref=ref,
                domain="stackoverflow.com",
                path="kubernetes",
                title="Intro to Kubernetes",
                active=True,
            )
        )
        assert bus.uow.websites.get("stackoverflow.com").find(ref) is not None
        bus.handle(
            commands.UpdateLink(
                ref=ref,
                domain="wikipedia.org",
                path=None,
                title=None,
                active=None,
            )
        )
        bus.uow.websites.get("stackoverflow.com").find(ref) is None
        link = bus.uow.websites.get("wikipedia.org").find(ref)
        assert link is not None
        assert link.ref == ref
        assert link.domain == "wikipedia.org"
        assert link.path == "kubernetes"
        assert link.title == "Intro to Kubernetes"
        assert link.active

    def test_update_all_attributes(self):
        ref = random_values.generate_ref()
        bus = message_bus()
        bus.handle(
            commands.RegisterLink(
                ref=ref,
                domain="stackoverflow.com",
                path="kubernetes",
                title="Intro to Kubernetes",
                active=True,
            )
        )
        assert bus.uow.websites.get("stackoverflow.com").find(ref) is not None
        bus.handle(
            commands.UpdateLink(
                ref=ref,
                domain="wikipedia.org",
                path="docker",
                title="Docker",
                active=False,
            )
        )
        bus.uow.websites.get("stackoverflow.com").find(ref) is None
        link = bus.uow.websites.get("wikipedia.org").find(ref)
        assert link is not None
        assert link.ref == ref
        assert link.domain == "wikipedia.org"
        assert link.path == "docker"
        assert link.title == "Docker"
        assert not link.active
