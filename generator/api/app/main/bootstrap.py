import inspect

from app.main.adapters import orm
from app.main.service_layer import unit_of_work, message_bus, handlers


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
) -> message_bus.MessageBus:

    if start_orm:
        orm.start_mappers()

    dependencies = {"uow": uow}
    injected_event_handlers = {
        event: [
            inject_dependencies(handler, dependencies) for handler in handlers
        ]
        for event, handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command: inject_dependencies(handler, dependencies)
        for command, handler in handlers.COMMAND_HANDLERS.items()
    }

    return message_bus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    handler_dependencies = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return handler(**handler_dependencies)
