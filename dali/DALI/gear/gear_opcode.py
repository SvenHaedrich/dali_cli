"""Control gear opcodes."""

from typing import Final


class GearLevelCommandOpcode:
    OFF: Final[int] = 0x00
    UP: Final[int] = 0x01
    DOWN: Final[int] = 0x02
    RECALL_MAX: Final[int] = 0x05
    RECALL_MIN: Final[int] = 0x06
    GOTO_SCENE: Final[int] = 0x10


class GearConfigureCommandOpcode:
    RESET: Final[int] = 0x20
    STORE_ACTUAL_LEVEL: Final[int] = 0x21
    SET_OPERATION_MODE: Final[int] = 0x23
    RESET_MEMORY_BANK: Final[int] = 0x24
    IDENTIFY_GEAR: Final[int] = 0x25
    SET_MAX_LEVEL: Final[int] = 0x2A
    SET_MIN_LEVEL: Final[int] = 0x2B
    SET_FAIL_LEVEL: Final[int] = 0x2C
    SET_POWER_ON_LEVEL: Final[int] = 0x2D
    SET_FADE_TIME: Final[int] = 0x2E
    SET_FADE_RATE: Final[int] = 0x2F
    SET_EXT_FADE: Final[int] = 0x30
    SET_SCENE: Final[int] = 0x40
    REMOVE_SCENE: Final[int] = 0x50
    ADD_GROUP: Final[int] = 0x60
    REMOVE_GROUP: Final[int] = 0x70
    SET_SHORT_ADR: Final[int] = 0x80
    ENABLE_WRITE: Final[int] = 0x81


class GearQueryCommandOpcode:
    STATUS: Final[int] = 0x90
    GEAR_PRESENT: Final[int] = 0x91
    LAMP_FAILURE: Final[int] = 0x92
    LAMP_POWER_ON: Final[int] = 0x93
    LIMIT_ERROR: Final[int] = 0x94
    RESET_STATE: Final[int] = 0x95
    MISSING_SHORT_ADDRESS: Final[int] = 0x96
    VERSION_NUMBER: Final[int] = 0x97
    CONTENT_DTR0: Final[int] = 0x98
    DEVICE_TYPE: Final[int] = 0x99
    PHYSICAL_MINIMUM: Final[int] = 0x9A
    POWER_FAILURE: Final[int] = 0x9B
    CONTENT_DTR1: Final[int] = 0x9C
    CONTENT_DTR2: Final[int] = 0x9D
    OPERATING_MODE: Final[int] = 0x9E
    LIGHT_SOURCE_TYPE: Final[int] = 0x9F
    ACTUAL_LEVEL: Final[int] = 0xA0
    MAX_LEVEL: Final[int] = 0xA1
    MIN_LEVEL: Final[int] = 0xA2
    POWER_ON_LEVEL: Final[int] = 0xA3
    SYSTEM_FAILURE_LEVEL: Final[int] = 0xA4
    FADE_TIME_RATE: Final[int] = 0xA5
    MANUFACTURER_SPECIFIC_MODE: Final[int] = 0xA6
    NEXT_DEVICE_TYPE: Final[int] = 0xA7
    EXTENDED_FADE_TIME: Final[int] = 0xA8
    GEAR_FAILURE: Final[int] = 0xAA
    SCENE_LEVEL: Final[int] = 0xB0
    GROUPS_0_7: Final[int] = 0xC0
    GROUPS_8_15: Final[int] = 0xC1
    RANDOM_ADDRESS_H: Final[int] = 0xC2
    RANDOM_ADDRESS_M: Final[int] = 0xC3
    RANDOM_ADDRESS_L: Final[int] = 0xC4
    READ_MEMORY: Final[int] = 0xC5
    EXTENDED_VERSION_NUMBER: Final[int] = 0xFF


class GearSpecialCommandOpcode:
    TERMINATE: Final[int] = 0xA1
    DTR0: Final[int] = 0xA3
    INITIALISE: Final[int] = 0xA5
    RANDOMISE: Final[int] = 0xA7
    COMPARE: Final[int] = 0xA9
    WITHDRAW: Final[int] = 0xAB
    PING: Final[int] = 0xAD
    SEARCHADDRH: Final[int] = 0xB1
    SEARCHADDRM: Final[int] = 0xB3
    SEARCHADDRL: Final[int] = 0xB5
    PROGRAM_SHORT_ADDRESS: Final[int] = 0xB7
    VERIFY_SHORT_ADDRESS: Final[int] = 0xB9
    QUERY_SHORT_ADDRESS: Final[int] = 0xBB
    ENABLE_DEVICE_TYPE: Final[int] = 0xC1
    DTR1: Final[int] = 0xC3
    DTR2: Final[int] = 0xC5
    WRITE: Final[int] = 0xC7
    WRITE_NR: Final[int] = 0xC9
