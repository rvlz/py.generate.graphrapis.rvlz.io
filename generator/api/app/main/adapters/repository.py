import abc

from app.main.domain import model
from app.main.adapters import orm


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, website: model.Website):
        self._add(website)
        self.seen.add(website)

    def get(self, domain: str) -> model.Website:
        website = self._get(domain)
        if website:
            self.seen.add(website)
        return website

    def get_by_linkref(self, linkref: str) -> model.Website:
        website = self._get_by_linkref(linkref)
        if website:
            self.seen.add(website)
        return website

    @abc.abstractmethod
    def _add(self, website: model.Website):
        pass

    @abc.abstractmethod
    def _get(self, domain: str) -> model.Website:
        pass

    @abc.abstractmethod
    def _get_by_linkref(self, linkref: str) -> model.Website:
        pass


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, website: model.Website):
        self.session.add(website)

    def _get(self, domain: str) -> model.Website:
        return (
            self.session.query(model.Website)
            .filter(orm.website.c.domain == domain)
            .first()
        )

    def _get_by_linkref(self, linkref: str) -> model.Website:
        return (
            self.session.query(model.Website)
            .join(model.Link)
            .filter(
                orm.link.c.ref == linkref,
            )
            .first()
        )
