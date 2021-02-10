from typing import List, TypedDict
from dataclasses import dataclass


class LinkType(TypedDict):
    ref: str
    domain: str
    path: str
    title: str
    deleted: bool


class Command:
    pass


@dataclass(frozen=True)
class RegisterLink(Command):
    ref: str
    domain: str
    path: str
    title: str


@dataclass(frozen=True)
class DeregisterLink(Command):
    ref: str


@dataclass(frozen=True)
class BulkCreateLinks(Command):
    links: List[LinkType]
