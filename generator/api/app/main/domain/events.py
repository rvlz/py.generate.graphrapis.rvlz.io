from dataclasses import dataclass


class Event:
    pass


@dataclass(frozen=True)
class LinkRegistered(Event):
    ref: str
    domain: str
    path: str
    title: str
    active: bool
