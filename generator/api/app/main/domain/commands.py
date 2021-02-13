from typing import List, TypedDict
from dataclasses import dataclass


class LinkType(TypedDict):
    ref: str
    domain: str
    path: str
    title: str


class Command:
    pass


@dataclass(frozen=True)
class RegisterLink(Command):
    ref: str
    domain: str
    path: str
    title: str
    active: bool = True


@dataclass(frozen=True)
class DeactivateLink(Command):
    ref: str


@dataclass(frozen=True)
class BulkRegisterLinks(Command):
    links: List[LinkType]
