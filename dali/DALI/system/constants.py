"""System constants"""

from enum import Enum, IntEnum


class DaliMax(IntEnum):
    """Maximum values from the DALI standards"""

    GROUP = 0x10
    SCENE = 0x10
    VALUE = 0x100
    ADR = 0x40
    BANK = 0x100
    PRIORITY = 5


class DaliTimeout(Enum):
    """Timeout for DALI frame transmission"""

    DEFAULT = 0.2


class DaliFrameLength(IntEnum):
    """Length for DALI frames"""

    BACKWARD = 8
    GEAR = 16
    DEVICE = 24


class DaliAddressingMode(Enum):
    """Addressing modes for DALI commands"""

    DAPC = "DAPC"
    SHORT = "SHORT"
    GROUP = "GROUP"
    BROADCAST = "BROADCAST"
    UNADDRESSED = "UNADDRESSED"
    SPECIAL = "SPECIAL"
    RESERVED = "RESERVED"
    INVALID = "INVALID"
