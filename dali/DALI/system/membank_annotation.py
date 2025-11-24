"""Print memory bank items with annotations."""

import click


# pylint: disable=too-few-public-methods
class MemoryBankItemWithAnnotation:
    """Print memory bank items with annotations"""

    annotations = {
        (0, 0): "address of last accessible memory location",
        (0, 1): "reserved",
        (0, 2): "number of last accessible memory bank",
        (0, 3): "GTIN byte 0 (MSB)",
        (0, 4): "GTIN byte 1",
        (0, 5): "GTIN byte 2",
        (0, 6): "GTIN byte 3",
        (0, 7): "GTIN byte 4",
        (0, 8): "GTIN byte 5 (LSB)",
        (0, 9): "firmware version (major)",
        (0, 10): "firmware version (minor)",
        (0, 11): "identification number byte 0 (MSB)",
        (0, 12): "identification number byte 1",
        (0, 13): "identification number byte 2",
        (0, 14): "identification number byte 3",
        (0, 15): "identification number byte 4",
        (0, 16): "identification number byte 5",
        (0, 17): "identification number byte 6",
        (0, 18): "identification number byte 7 (LSB)",
        (0, 19): "hardware version (major)",
        (0, 20): "hardware version (minor)",
        (0, 21): "101 version number",
        (0, 22): "102 version number",
        (0, 23): "103 version number",
        (0, 24): "number of logical control device units",
        (0, 25): "number of logical control gear units",
        (0, 26): "index number of logical gear unit",
        (0, 27): "current bus unit configuration",
        (1, 3): "OEM GTIN byte 0 (MSB)",
        (1, 4): "OEM GTIN byte 1",
        (1, 5): "OEM GTIN byte 2",
        (1, 6): "OEM GTIN byte 3",
        (1, 7): "OEM GTIN byte 4",
        (1, 8): "OEM GTIN byte 5 (LSB)",
        (1, 9): "OEM identification number byte 0 (MSB)",
        (1, 10): "OEM identification number byte 1",
        (1, 11): "OEM identification number byte 2",
        (1, 12): "OEM identification number byte 3",
        (1, 13): "OEM identification number byte 4",
        (1, 14): "OEM identification number byte 5",
        (1, 15): "OEM identification number byte 6",
        (1, 16): "OEM identification number byte 7 (LSB)",
        (202, 3): "version of the memory bank",
        (202, 4): "scale factor for active energy, expressed as power of 10",
        (202, 5): "active energy / Wh 0 (MSB)",
        (202, 6): "active energy / Wh 1",
        (202, 7): "active energy / Wh 2",
        (202, 8): "active energy / Wh 3",
        (202, 9): "active energy / Wh 4",
        (202, 10): "active energy / Wh 5 (LSB)",
        (202, 11): "scale factor for active power, expressed as power of 10",
        (202, 12): "active power / W 0 (MSB)",
        (202, 13): "active power / W 1",
        (202, 14): "active power / W 2",
        (202, 15): "active power / W 3 ( LSB)",
        (203, 3): "version of the memory bank",
        (203, 4): "scale factor for apparent energy, expressed as power of 10",
        (203, 5): "apparent energy / Wh 0 (MSB)",
        (203, 6): "apparent energy / Wh 1",
        (203, 7): "apparent energy / Wh 2",
        (203, 8): "apparent energy / Wh 3",
        (203, 9): "apparent energy / Wh 4",
        (203, 10): "apparent energy / Wh 5 (LSB)",
        (203, 11): "scale factor for apparent power, expressed as power of 10",
        (203, 12): "apparent power / W 0 (MSB)",
        (203, 13): "apparent power / W 1",
        (203, 14): "apparent power / W 2",
        (203, 15): "apparent power / W 3 (LSB)",
        (204, 3): "version of the memory bank",
        (204, 4): "scale factor for loadside energy, expressed as power of 10",
        (204, 5): "active energy loadside / Wh 0 (MSB)",
        (204, 6): "active energy loadside / Wh 1",
        (204, 7): "active energy loadside / Wh 2",
        (204, 8): "active energy loadside / Wh 3",
        (204, 9): "active energy loadside / Wh 4",
        (204, 10): "active energy loadside 5 / Wh (LSB)",
        (204, 11): "scale factor for loadside power, expressed as power of 10",
        (204, 12): "active power loadside / W 0 (MSB)",
        (204, 13): "active power loadside / W 1",
        (204, 14): "active power loadside / W 2",
        (204, 15): "active power loadside / W 3 (LSB)",
        (205, 3): "version of the memory bank",
        (205, 4): "control gear operating time / 1 s (MSB)",
        (205, 5): "control gear operating time / 1 s",
        (205, 6): "control gear operating time / 1 s",
        (205, 7): "control gear operating time / 1 s (LSB)",
        (205, 8): "control gear start counter (MSB)",
        (205, 9): "control gear start counter",
        (205, 10): "control gear start counter (LSB)",
        (205, 11): "control gear external supply voltage / 0.1 Vrms (MSB)",
        (205, 12): "control gear external supply voltage / 0.1 Vrms (LSB)",
        (205, 13): "control gear external supply frequency / 1 Hz",
        (205, 14): "control gear power factor / 0.01",
        (205, 15): "control gear overall failure condition",
        (205, 16): "control gear overall failure condition counter",
        (205, 17): "control gear external supply undervoltage",
        (205, 18): "control gear external supply undervoltage counter",
        (205, 19): "control gear external supply overvoltage",
        (205, 20): "control gear external supply overvoltage counter",
        (205, 21): "control gear output power limitation",
        (205, 22): "control gear output power limitation counter",
        (205, 23): "control gear thermal derating",
        (205, 24): "control gear thermal derating counter",
        (205, 25): "control gear thermal shutdown",
        (205, 26): "control gear thermal shutdown counter",
        (205, 27): "control gear temperature / 1 C offset 60",
        (205, 28): "control gear output current percent / 1 %",
        (206, 3): "version of the memory bank",
        (206, 4): "light source start counter resetable (MSB)",
        (206, 5): "light source start counter resetable",
        (206, 6): "light source start counter resetable (LSB)",
        (206, 7): "light source start counter (MSB)",
        (206, 8): "light source start counter",
        (206, 9): "light source start counter (LSB)",
        (206, 10): "light source on time resetable / 1 s (MSB)",
        (206, 11): "light source on time resetable / 1 s",
        (206, 12): "light source on time resetable / 1 s",
        (206, 13): "light source on time resetable / 1 s (LSB)",
        (206, 14): "light source on time / 1 s (MSB)",
        (206, 15): "light source on time / 1 s",
        (206, 16): "light source on time / 1 s",
        (206, 17): "light source on time / 1 s (LSB)",
        (206, 18): "light source voltage / 0.1 V (MSB)",
        (206, 19): "light source voltage / 0.1 V (LSB)",
        (206, 20): "light source current / 0.001 A (MSB)",
        (206, 21): "light source current / 0.001 A (LSB)",
        (206, 22): "light source overall failure condition",
        (206, 23): "light source overall failure condition counter",
        (206, 24): "light source short circuit",
        (206, 25): "light source short circuit counter",
        (206, 26): "light source open circuit",
        (206, 27): "light source open circuit counter",
        (206, 28): "light source thermal derating",
        (206, 29): "light source thermal derating counter",
        (206, 30): "light source thermal shutdown",
        (206, 31): "light source thermal shutdown counter",
        (206, 32): "light source temperature / 1 C, offset 60",
    }

    @staticmethod
    def show(bank: int, location: int, value: int | None):
        if bank != 0 and location == 0:
            annotation = MemoryBankItemWithAnnotation.annotations[(0, 0)]
        elif bank != 0 and location == 1:
            annotation = "indicator byte"
        elif bank != 0 and location == 2:
            annotation = "memory lock byte (0x55 = write-enabled)"
        else:
            annotation = MemoryBankItemWithAnnotation.annotations.get(
                (bank, location), " "
            )
        if value is None:
            click.echo(f"0x{location:02X} : NO - timeout {annotation}")
        else:
            if 0x20 < value:
                ascii_presentation = chr(value)
            else:
                ascii_presentation = chr(0x20)
            click.echo(
                f"0x{location:02X} : 0x{value:02X} = {value:3} = ´{ascii_presentation}´ {annotation}"
            )
