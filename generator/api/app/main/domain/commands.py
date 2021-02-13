from typing import List, TypedDict, Optional
from dataclasses import dataclass


class LinkType(TypedDict):
    ref: str
    domain: str
    path: str
    title: str
    active: bool


class Command:
    pass


@dataclass(frozen=True)
class RegisterLink(Command):
    ref: str
    domain: str
    path: str
    title: str
    active: bool


@dataclass(frozen=True)
class DeactivateLink(Command):
    ref: str


@dataclass(frozen=True)
class BulkRegisterLinks(Command):
    links: List[LinkType]


@dataclass(frozen=True)
class UpdateLink(Command):
    ref: str
    domain: Optional[str]
    path: Optional[str]
    title: Optional[str]
    active: Optional[str]
