from typing import List


class Link:
    def __init__(
        self,
        ref: str,
        domain: str,
        path: str,
        title: str,
        deleted: bool = False,
    ):
        self.ref = ref
        self.domain = domain
        self.path = path
        self.title = title
        self.deleted = deleted

    def __hash__(self):
        return hash(self.ref)

    def __eq__(self, other):
        if not isinstance(other, Link):
            return False
        return other.ref == self.ref

    def delete(self):
        self.deleted = True


class Website:
    def __init__(self, domain: str, links: List[Link] = []):
        self.domain = domain
        self.links = links
        self.events = []

    def register(self, links: List[Link]):
        self.links = self.links + links

    def registered(self, link: Link):
        return link in self.links

    def can_register(self, link: Link):
        return link.domain == self.domain

    def find(self, linkref: str):
        return next(
            (link for link in self.links if link.ref == linkref),
            None,
        )
