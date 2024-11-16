"""Control device addressing class."""

from typing import Final

from typeguard import typechecked

from ..system.constants import DaliMax


@typechecked
class DaliDeviceAddressByte:
    SHORT: Final[str] = "SHORT"
    GROUP: Final[str] = "GROUP"
    BROADCAST: Final[str] = "BROADCAST"
    UNADDRESSED: Final[str] = "UNADDRESSED"
    SPECIAL: Final[str] = "SPECIAL"
    RESERVED: Final[str] = "RESERVED"
    INVALID: Final[str] = "INVALID"

    def __init__(self) -> None:
        self.byte = 0x01
        self.mode = self.INVALID

    def short(self, address: int = 0) -> None:
        if 0 <= address < DaliMax.ADR:
            self.byte = 0x01
            self.byte |= address << 1
            self.mode = self.SHORT

    def group(self, group: int = 0) -> None:
        if 0 <= group < DaliMax.GROUP:
            self.byte = group << 1
            self.byte |= 0x81
            self.mode = self.GROUP

    def broadcast(self) -> None:
        self.byte = 0xFF
        self.mode = self.BROADCAST

    def unaddressed(self) -> None:
        self.byte = 0xFD
        self.mode = self.UNADDRESSED

    def special(self, code: int = 0) -> None:
        self.byte &= 0x01
        if 0 < code < 16:
            self.byte = code << 1
            self.byte |= 0xC1
            self.mode = self.SPECIAL

    def arg(self, text: str = "") -> bool:
        text = text.upper()
        if text == "BC":
            self.broadcast()
            return True
        if text == "BCU":
            self.unaddressed()
            return True
        if text[0] == "G":
            g = int(text[1:3])
            if 0 <= g < DaliMax.GROUP:
                self.group(g)
                return True
            else:
                return False
        s = int(text)
        if 0 <= s < Dali.ADR:
            self.short(s)
            return True
        return False

    def __str__(self) -> str:
        if self.mode == self.SHORT:
            short_address = (self.byte >> 1) & 0x3F
            return f"D{short_address:02}"
        elif self.mode == self.GROUP:
            group_address = (self.byte >> 1) & 0xF
            return f"DG{group_address:02}"
        else:
            return self.mode
