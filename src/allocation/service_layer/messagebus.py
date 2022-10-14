from __future__ import annotations
from functools import singledispatchmethod
import logging
from typing import Callable, TYPE_CHECKING

from allocation.domain import commands, events

if TYPE_CHECKING:
    from . import unit_of_work


logger = logging.getLogger(__name__)

Message = commands.Command | events.Event


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: dict[type[events.Event], list[Callable]],
        command_handlers: dict[type[commands.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            self._handle(message)
 
    @singledispatchmethod
    def _handle(self, message):
        raise Exception(f"{message} was not an Event or Command")
    
    @_handle.register
    def _(self, message: events.Event):
        self.handle_event(message)

    @_handle.register
    def _(self, message: commands.Command):
        self.handle_command(message)
    
    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    def handle_command(self, command: commands.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise
