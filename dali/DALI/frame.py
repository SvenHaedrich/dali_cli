from typing import NamedTuple


class DaliTxFrame(NamedTuple):
    length: int
    data: int
    send_twice: bool = False
    priority: int = 1


class DaliRxFrame(NamedTuple):
    COMMAND = 1
    ERROR = 2

    timestamp: int = 0
    type: int = 0
    length: int = 0
    data: int = 0
