"""Connection resource to handle the connection with click"""

from contextlib import contextmanager

import click
from dali_interface import (
    DaliFrame,
    DaliInterface,
    DaliMock,
    DaliSerial,
    DaliUsb,
)


class DaliNone(DaliInterface):
    """This is used when no other connection is selected."""

    def __init__(self):
        super().__init__(start_receive=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.close()

    def transmit(self, _frame: DaliFrame, _block: bool) -> None:
        print("no interface defined -- command lost")

    def close(self):
        pass


@contextmanager
def dali_connection(connection_type: str, serial_port: None | str = None):  # pylint disable=raise-missing-from
    try:
        if connection_type == "None":
            resource = DaliNone()
        elif connection_type == "Serial":
            resource = DaliSerial(portname=serial_port)
        elif connection_type == "Usb":
            resource = DaliUsb()
        elif connection_type == "Mock":
            resource = DaliMock()
        else:
            raise click.BadArgumentUsage("no valid DALI connection selected.")
    except Exception as error:
        raise click.BadArgumentUsage("can not open connection.") from error
    yield resource
    resource.close()
