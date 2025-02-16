"""Control device addressing class."""

from enum import Enum, unique

from typeguard import typechecked

from ..system.constants import DaliMax


@unique
class DeviceAddressing(Enum):
    """Addressing modes for control device commands, see iec 62386-103:2022 Table 1"""

    INVALID = 0
    SHORT = 1
    GROUP = 2
    BROADCAST = 3
    UNADDRESSED = 4
    SPECIAL = 5


@typechecked
class DeviceAddress:
    """Interfaces between DALI address mode and frame codes"""

    def __init__(self, mode="BC") -> None:
        self.mode = DeviceAddressing.INVALID
        self.byte = 0
        if mode == "SPECIAL":
            self.special()
            return
        if self.arg(mode):
            return
        raise ValueError("invalid addressing mode")

    def short(self, address: int = 0) -> None:
        """Short addressing"""
        if 0 <= address < DaliMax.ADR:
            self.byte = 0x01
            self.byte |= address << 1
            self.mode = DeviceAddressing.SHORT

    def group(self, group: int = 0) -> None:
        """Device group addressing"""
        if 0 <= group < DaliMax.DEVICE_GROUP:
            self.byte = group << 1
            self.byte |= 0x81
            self.mode = DeviceAddressing.GROUP

    def broadcast(self) -> None:
        """Broadcast"""
        self.byte = 0xFF
        self.mode = DeviceAddressing.BROADCAST

    def unaddressed(self) -> None:
        """Broadcast unaddressed"""
        self.byte = 0xFD
        self.mode = DeviceAddressing.UNADDRESSED

    def special(self, code: int = 0) -> None:
        """Special command"""
        self.byte &= 0x01
        if 0 <= code < 16:
            self.byte = code << 1
            self.byte |= 0xC1
            self.mode = DeviceAddressing.SPECIAL

    def isvalid(self) -> bool:
        """Check if control device addressing mode is valid"""
        return self.mode != DeviceAddressing.INVALID

    def arg(self, text: str = "") -> bool:
        """Scan from command line parameter"""
        text = text.upper()
        if text == "BC":
            self.broadcast()
            return True
        if text == "BCU":
            self.unaddressed()
            return True
        if text[0] == "G":
            g = int(text[1:3])
            if 0 <= g < DaliMax.DEVICE_GROUP:
                self.group(g)
                return True
            return False
        s = int(text)
        if 0 <= s < DaliMax.ADR:
            self.short(s)
            return True
        return False

    def __str__(self) -> str:
        if self.mode == DeviceAddressing.SHORT:
            short_address = (self.byte >> 1) & 0x3F
            return f"D{short_address:02}"
        if self.mode == DeviceAddressing.GROUP:
            group_address = (self.byte >> 1) & 0xF
            return f"DG{group_address:02}"
        return self.mode.value


@unique
class InstanceAddressing(Enum):
    """Addressing modes for device instances, see iec 62386-103:2022 Table 2"""

    INVALID = 0
    INSTANCE_NUMBER = 1
    INSTANCE_GROUP = 2
    INSTANCE_TYPE = 3
    FEATURE_INSTANCE_NUMBER = 4
    FEATURE_INSTANCE_GROUP = 5
    FEATURE_INSTANCE_TYPE = 6
    FEATURE_BROADCAST = 7
    FEATURE_INSTANCE_BROADCAST = 8
    INSTANCE_BROADCAST = 9
    FEATURE_DEVICE = 10
    DEVICE = 11


@typechecked
class InstanceAddress:
    """Interfaces between DALI addressing representation and command addressing format"""

    def __init__(self) -> None:
        self.mode = InstanceAddressing.INVALID
        self.byte = 0
        self.device()

    def instance_number(self, number: int = 0) -> None:
        """Instance number addressing"""
        if 0 <= number < DaliMax.INSTANCE_NUMBER:
            self.byte = number
            self.mode = InstanceAddressing.INSTANCE_NUMBER

    def instance_group(self, group: int = 0) -> None:
        """Instance group addressing"""
        if 0 <= group < DaliMax.INSTANCE_GROUP:
            self.byte = group | 0x80
            self.mode = InstanceAddressing.INSTANCE_NUMBER

    def instance_type(self, type: int = 0) -> None:
        """Instance type addressing"""
        if 0 <= type < DaliMax.INSTANCE_TYPES:
            self.byte = type | 0xC0
            self.mode = InstanceAddressing.INSTANCE_TYPE

    def device(self) -> None:
        self.byte = 0xFE
        self.mode = InstanceAddressing.DEVICE
