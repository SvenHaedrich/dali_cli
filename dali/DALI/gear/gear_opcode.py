"""Control gear opcodes."""

from enum import IntEnum


class GearLevelCommandOpcode(IntEnum):
    """Control gear level command opcodes IEC 62386-102:2022 11.3"""

    OFF = 0x00
    UP = 0x01
    DOWN = 0x02
    RECALL_MAX = 0x05
    RECALL_MIN = 0x06
    GOTO_SCENE = 0x10


class GearConfigureCommandOpcode(IntEnum):
    """Control gear configure command opcodes IEC 62386-102:2022 11.4"""

    RESET = 0x20
    STORE_ACTUAL_LEVEL = 0x21
    SET_OPERATION_MODE = 0x23
    RESET_MEMORY_BANK = 0x24
    IDENTIFY_GEAR = 0x25
    SET_MAX_LEVEL = 0x2A
    SET_MIN_LEVEL = 0x2B
    SET_FAIL_LEVEL = 0x2C
    SET_POWER_ON_LEVEL = 0x2D
    SET_FADE_TIME = 0x2E
    SET_FADE_RATE = 0x2F
    SET_EXT_FADE = 0x30
    SET_SCENE = 0x40
    REMOVE_SCENE = 0x50
    ADD_GROUP = 0x60
    REMOVE_GROUP = 0x70
    SET_SHORT_ADR = 0x80
    ENABLE_WRITE = 0x81


class GearQueryCommandOpcode(IntEnum):
    """Control gear query command opcodes IEC 62386-102:2022 11.5"""

    STATUS = 0x90
    GEAR_PRESENT = 0x91
    LAMP_FAILURE = 0x92
    LAMP_POWER_ON = 0x93
    LIMIT_ERROR = 0x94
    RESET_STATE = 0x95
    MISSING_SHORT_ADDRESS = 0x96
    VERSION_NUMBER = 0x97
    CONTENT_DTR0 = 0x98
    DEVICE_TYPE = 0x99
    PHYSICAL_MINIMUM = 0x9A
    POWER_FAILURE = 0x9B
    CONTENT_DTR1 = 0x9C
    CONTENT_DTR2 = 0x9D
    OPERATING_MODE = 0x9E
    LIGHT_SOURCE_TYPE = 0x9F
    ACTUAL_LEVEL = 0xA0
    MAX_LEVEL = 0xA1
    MIN_LEVEL = 0xA2
    POWER_ON_LEVEL = 0xA3
    SYSTEM_FAILURE_LEVEL = 0xA4
    FADE_TIME_RATE = 0xA5
    MANUFACTURER_SPECIFIC_MODE = 0xA6
    NEXT_DEVICE_TYPE = 0xA7
    EXTENDED_FADE_TIME = 0xA8
    GEAR_FAILURE = 0xAA
    SCENE_LEVEL = 0xB0
    GROUPS_0_7 = 0xC0
    GROUPS_8_15 = 0xC1
    RANDOM_ADDRESS_H = 0xC2
    RANDOM_ADDRESS_M = 0xC3
    RANDOM_ADDRESS_L = 0xC4
    READ_MEMORY = 0xC5
    EXTENDED_VERSION_NUMBER = 0xFF


class GearSpecialCommandOpcode(IntEnum):
    """Control gear level command opcodes IEC 62386-102:2022 11.7"""

    TERMINATE = 0xA1
    DTR0 = 0xA3
    INITIALISE = 0xA5
    RANDOMISE = 0xA7
    COMPARE = 0xA9
    WITHDRAW = 0xAB
    PING = 0xAD
    SEARCHADDRH = 0xB1
    SEARCHADDRM = 0xB3
    SEARCHADDRL = 0xB5
    PROGRAM_SHORT_ADDRESS = 0xB7
    VERIFY_SHORT_ADDRESS = 0xB9
    QUERY_SHORT_ADDRESS = 0xBB
    ENABLE_DEVICE_TYPE = 0xC1
    DTR1 = 0xC3
    DTR2 = 0xC5
    WRITE = 0xC7
    WRITE_NR = 0xC9
