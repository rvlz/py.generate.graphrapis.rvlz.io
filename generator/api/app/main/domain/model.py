from typing import List

from app.main.domain import events


class Link:
    def __init__(
        self,
        ref: str,
        domain: str,
        path: str,
        title: str,
        active: bool = True,
    ):
        self.ref = ref
        self.domain = domain
        self.path = path
        self.title = title
        self.active = active

    def __hash__(self):
        return hash(self.ref)

    def __eq__(self, other):
        if not isinstance(other, Link):
            return False
        return other.ref == self.ref

    def deactivate(self):
        self.active = False


class Website:
    def __init__(self, domain: str, links: List[Link] = []):
        self.domain = domain
        self.links = links
        self.events = []

    def register(self, links: List[Link]):
        self.links += links
        self.events += [
            events.LinkRegistered(
                ref=link.ref,
                domain=link.domain,
                path=link.path,
                title=link.title,
                active=link.active,
            )
            for link in links
        ]

    def registered(self, link: Link):
        return link in self.links

    def can_register(self, link: Link):
        return link.domain == self.domain

    def find(self, linkref: str):
        return next(
            (
                link
                for link in self.links
                if link.domain is not None and link.ref == linkref
            ),
            None,
        )

    def remove(self, linkref: str):
        for link in self.links:
            if link.ref == linkref:
                self.links.remove(link)
                return link
