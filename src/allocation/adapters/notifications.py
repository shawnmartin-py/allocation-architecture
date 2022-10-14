from abc import ABC, abstractmethod
import smtplib

from allocation import config


class AbstractNotifications(ABC):
    @abstractmethod
    def send(self, destination, message): ...


DEFAULT_HOST = config.get_email_host_and_port()["host"]  # type: str
DEFAULT_PORT = config.get_email_host_and_port()["port"]  # type: int


class EmailNotifications(AbstractNotifications):
    def __init__(self, smtp_host = DEFAULT_HOST, port = DEFAULT_PORT):
        self.server = smtplib.SMTP(smtp_host, port=port)
        self.server.noop()

    def send(self, destination: str, message: str):
        msg = f"Subject: allocation service notification\n{message}"
        self.server.sendmail(
            from_addr="allocations@example.com",
            to_addrs=[destination],
            msg=msg,
        )
