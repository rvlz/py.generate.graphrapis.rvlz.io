import abc

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from app.main.adapters import repository
from app.main.service_layer import errors
from app.main import config


class AbstractUnitOfWork(abc.ABC):
    websites: repository.AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass

    def collect_new_events(self):
        for website in self.websites.seen:
            while website.events:
                yield website.events.pop(0)


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_database_uri(),
        isolation_level="REPEATABLE READ",
    )
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.websites = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        try:
            self.session.commit()
        except IntegrityError as exc:
            _, resource, field = exc.orig.diag.constraint_name.split("_")
            value = exc.params[field]
            raise errors.DuplicateFieldError(
                resource=resource,
                field=field,
                value=value,
            )

    def rollback(self):
        self.session.rollback()
