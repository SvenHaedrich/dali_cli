"""Control device opcodes."""

from typing import Final


class DeviceConfigureCommandOpcode:
    IDENTIFY_DEVICE: Final[int] = 0x00
    RESET_POWER_CYCLE_SEEN: Final[int] = 0x02
    RESET: Final[int] = 0x10
    RESET_MEMORY_BANK: Final[int] = 0x11


class DeviceQueryCommandOpcode:
    QUERY_STATUS: Final[int] = 0x30
    QUERY_APPLICATION_CONTROLLER_ERROR: Final[int] = 0x31
    QUERY_INPUT_DEVICE_ERROR: Final[int] = 0x32
    QUERY_MISSING_SHORT_ADDRESS: Final[int] = 0x33
    QUERY_VERSION_NUMBER: Final[int] = 0x34
    QUERY_NUMBER_OF_INSTANCES: Final[int] = 0x35
    QUERY_CONTENT_DTR0: Final[int] = 0x36
    QUERY_CONTENT_DTR1: Final[int] = 0x37
    QUERY_CONTENT_DTR2: Final[int] = 0x38
    QUERY_DEVICE_CAPABILITIES: Final[int] = 0x46
    READ_MEMORY: Final[int] = 0x3C


class DeviceSpecialCommandOpcode:
    TERMINATE: Final[int] = 0x00
    INITIALISE: Final[int] = 0x01
    RANDOMISE: Final[int] = 0x02
    COMPARE: Final[int] = 0x03
    WITHDRAW: Final[int] = 0x04
    SEARCHADDRH: Final[int] = 0x05
    SEARCHADDRM: Final[int] = 0x06
    SEARCHADDRL: Final[int] = 0x07
    PROGRAM_SHORT_ADDRESS: Final[int] = 0x08
    VERIFY_SHORT_ADDRESS: Final[int] = 0x09
    QUERY_SHORT_ADDRESS: Final[int] = 0x0A
    WRITE_MEMORY: Final[int] = 0x20
    WRITE_MEMORY_NO_REPLY: Final[int] = 0x21
    DTR0: Final[int] = 0x30
    DTR1: Final[int] = 0x31
    DTR2: Final[int] = 0x32
    SEND_TESTFRAME: Final[int] = 0x33
    DIRECT_WRITE_MEMORY: Final[int] = 0xC5
    DTR1_DTR0: Final[int] = 0xC7
    DTR2_DTR1: Final[int] = 0xC9
