from typing import Dict, List, Callable, Type, Union

from app.main.service_layer import unit_of_work
from app.main.domain import events, commands

Message = Union[events.Event, commands.Command]


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                self.handle_command(message)
            else:
                raise Exception(f"{message} not a event or command.")

    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                continue

    def handle_command(self, command: commands.Command):
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception as exc:
            raise exc
