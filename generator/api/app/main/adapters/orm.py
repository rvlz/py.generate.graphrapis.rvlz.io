import datetime

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    event,
)
from sqlalchemy.orm import relationship, mapper

from app.main.domain import model

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

website = Table(
    "website",
    metadata,
    Column("domain", String(255), primary_key=True),
)

link = Table(
    "link",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ref", String, unique=True),
    Column("domain", ForeignKey("website.domain")),
    Column("path", Text),
    Column("title", String(255)),
    Column("active", Boolean, default=True),
)


link_view = Table(
    "link_view",
    metadata,
    Column("ref", String(255)),
    Column("domain", String(255)),
    Column("path", Text),
    Column("title", String(255)),
    Column("active", Boolean),
    Column("created_at", DateTime),
)


def start_mappers():
    link_mapper = mapper(model.Link, link)
    mapper(
        model.Website, website, properties={"links": relationship(link_mapper)}
    )


@event.listens_for(model.Website, "load")
def receive_load(website, _):
    website.events = []
