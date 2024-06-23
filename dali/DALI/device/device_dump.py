import click
import dali

from .device_action import query_device_value, set_device_dtr0, set_device_dtr1
from .device_opcode import DeviceQueryCommandOpcode


def device_show_memory_content(bank, location, value):
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
    }
    if bank != 0 and location == 0:
        annotation = annotations[(0, 0)]
    elif bank != 0 and location == 1:
        annotation = "indicactor byte"
    elif bank != 0 and location == 2:
        annotation = "memory lock byte (0x55 = write-enabled)"
    else:
        annotation = annotations.get((bank, location), " ")
    if value is None:
        click.echo(f"0x{location:02X} : NO - timeout {annotation}")
    else:
        if 0x20 < value:
            ascii = chr(value)
        else:
            ascii = chr(0x20)
        click.echo(f"0x{location:02X} : 0x{value:02X} = {value:3} = ´{ascii}´ {annotation}")


@click.command(name="dump", help="Dump contents of a memory bank.")
@click.argument("bank", type=click.INT)
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)
def dump(adr, bank):
    set_device_dtr1(bank, "BANK")
    set_device_dtr0(0, "LOCATION")
    last_accessible_location = query_device_value(
        adr, DeviceQueryCommandOpcode.READ_MEMORY, close=False
    )
    if last_accessible_location is None:
        click.echo(f"memory bank {bank} not implemented")
        dali.connection.close()
        return
    device_show_memory_content(bank, 0, last_accessible_location)
    for location in range(1, last_accessible_location + 1):
        device_show_memory_content(
            bank,
            location,
            query_device_value(adr, DeviceQueryCommandOpcode.READ_MEMORY, close=False),
        )
    dali.connection.close()
