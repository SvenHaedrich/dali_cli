"""Class for control gear addressing."""

from typing import Final

import dali
from typeguard import typechecked


@typechecked
class DaliAddressByte:
    DAPC: Final[str] = "DAPC"
    SHORT: Final[str] = "SHORT"
    GROUP: Final[str] = "GROUP"
    BROADCAST: Final[str] = "BROADCAST"
    UNADDRESSED: Final[str] = "UNADDRESSED"
    SPECIAL: Final[str] = "SPECIAL"
    RESERVED: Final[str] = "RESERVED"
    INVALID: Final[str] = "INVALID"

    def __init__(self, dapc: bool = False) -> None:
        if dapc:
            self.byte = 0x00
        else:
            self.byte = 0x01
        self.mode = self.INVALID

    def short(self, address: int = 0) -> None:
        if 0 <= address < DaliMax.ADR:
            self.byte &= 0x01
            self.byte |= address << 1
            self.mode = self.SHORT

    def group(self, group: int = 0) -> None:
        if 0 <= group < DaliMax.GROUP:
            self.byte &= 0x01
            self.byte |= group << 1
            self.byte |= 0x80
            self.mode = self.GROUP

    def broadcast(self) -> None:
        self.byte &= 0x01
        self.byte |= 0xFE
        self.mode = self.BROADCAST

    def unaddressed(self) -> None:
        self.byte &= 0x01
        self.byte |= 0xFC
        self.mode = self.UNADDRESSED

    def special(self, code: int = 0) -> None:
        self.byte &= 0x01
        if code in range(0xA0, 0xCC):
            self.byte |= code
            self.mode = self.SPECIAL

    def reserved(self, code: int = 0) -> None:
        self.byte &= 0x01
        if code in range(0xCC, 0xFC):
            self.byte |= code
            self.mode = self.RESERVED

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
            if g in range(16):
                self.group(g)
                return True
            else:
                return False
        s = int(text)
        if s in range(DaliMax.ADR):
            self.short(s)
            return True
        return False

    def __str__(self) -> str:
        if self.mode == self.SHORT:
            short_address = (self.byte >> 1) & 0x3F
            return f"G{short_address:02}"
        elif self.mode == self.GROUP:
            group_address = (self.byte >> 1) & 0xF
            return f"GG{group_address:02}"
        else:
            return self.mode
