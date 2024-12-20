"""Control device opcodes."""

from enum import IntEnum


class DeviceConfigureCommandOpcode(IntEnum):
    """Control device configuration command opcodes IEC 62386-103:2022 11.5"""

    IDENTIFY_DEVICE = 0x00
    RESET_POWER_CYCLE_SEEN = 0x02
    RESET = 0x10
    RESET_MEMORY_BANK = 0x11


class DeviceQueryCommandOpcode(IntEnum):
    """Control device query command opcodes IEC 62386-103:2022 11.6"""

    QUERY_STATUS = 0x30
    QUERY_APPLICATION_CONTROLLER_ERROR = 0x31
    QUERY_INPUT_DEVICE_ERROR = 0x32
    QUERY_MISSING_SHORT_ADDRESS = 0x33
    QUERY_VERSION_NUMBER = 0x34
    QUERY_NUMBER_OF_INSTANCES = 0x35
    QUERY_CONTENT_DTR0 = 0x36
    QUERY_CONTENT_DTR1 = 0x37
    QUERY_CONTENT_DTR2 = 0x38
    QUERY_DEVICE_CAPABILITIES = 0x46
    READ_MEMORY = 0x3C


class DeviceSpecialCommandOpcode(IntEnum):
    """Control device special command opcodes IEC 62386-103:2022 11.10"""

    TERMINATE = 0x00
    INITIALISE = 0x01
    RANDOMISE = 0x02
    COMPARE = 0x03
    WITHDRAW = 0x04
    SEARCHADDRH = 0x05
    SEARCHADDRM = 0x06
    SEARCHADDRL = 0x07
    PROGRAM_SHORT_ADDRESS = 0x08
    VERIFY_SHORT_ADDRESS = 0x09
    QUERY_SHORT_ADDRESS = 0x0A
    WRITE_MEMORY = 0x20
    WRITE_MEMORY_NO_REPLY = 0x21
    DTR0 = 0x30
    DTR1 = 0x31
    DTR2 = 0x32
    SEND_TESTFRAME = 0x33
    DIRECT_WRITE_MEMORY = 0xC5
    DTR1_DTR0 = 0xC7
    DTR2_DTR1 = 0xC9
