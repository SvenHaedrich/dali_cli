"""Class for control gear addressing."""

from typeguard import typechecked

from ..system.constants import DaliAddressingMode, DaliMax


@typechecked
class GearAddress:
    """Class for control gear addressing."""

    def __init__(self, dapc: bool = False) -> None:
        if dapc:
            self.byte = 0x00
        else:
            self.byte = 0x01
        self.mode = DaliAddressingMode.INVALID

    def short(self, address: int = 0) -> None:
        if 0 <= address < DaliMax.ADR:
            self.byte &= 0x01
            self.byte |= address << 1
            self.mode = DaliAddressingMode.SHORT

    def group(self, group: int = 0) -> None:
        if 0 <= group < DaliMax.GEAR_GROUP:
            self.byte &= 0x01
            self.byte |= group << 1
            self.byte |= 0x80
            self.mode = DaliAddressingMode.GROUP

    def broadcast(self) -> None:
        self.byte &= 0x01
        self.byte |= 0xFE
        self.mode = DaliAddressingMode.BROADCAST

    def unaddressed(self) -> None:
        self.byte &= 0x01
        self.byte |= 0xFC
        self.mode = DaliAddressingMode.UNADDRESSED

    def special(self, code: int = 0) -> None:
        self.byte &= 0x01
        if code in range(0xA0, 0xCC):
            self.byte |= code
            self.mode = DaliAddressingMode.SPECIAL

    def reserved(self, code: int = 0) -> None:
        self.byte &= 0x01
        if code in range(0xCC, 0xFC):
            self.byte |= code
            self.mode = DaliAddressingMode.RESERVED

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
            if 0 <= g < DaliMax.GEAR_GROUP:
                self.group(g)
                return True
            return False
        s = int(text)
        if s in range(DaliMax.ADR):
            self.short(s)
            return True
        return False

    def __str__(self) -> str:
        if self.mode == DaliAddressingMode.SHORT:
            short_address = (self.byte >> 1) & 0x3F
            return f"G{short_address:02}"
        if self.mode == DaliAddressingMode.GROUP:
            group_address = (self.byte >> 1) & 0xF
            return f"GG{group_address:02}"
        return self.mode.value
