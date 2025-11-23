"""Control device dump memory bank content."""

import click
from dali_interface import DaliInterface

from ..system.membank_annotation import MemoryBankItemWithAnnotation
from .device_action import query_device_value, set_device_dtr0, set_device_dtr1
from .device_opcode import DeviceQueryCommandOpcode


@click.command(name="dump", help="Dump contents of a memory bank.")
@click.pass_obj
@click.argument("bank", type=click.INT)
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)
def dump(dali: DaliInterface, adr, bank):
    set_device_dtr1(dali, bank)
    set_device_dtr0(dali, 0)
    last_accessible_location = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.READ_MEMORY
    )
    if last_accessible_location is None:
        click.echo(f"memory bank {bank} not implemented")
        return
    MemoryBankItemWithAnnotation.show(bank, 0, last_accessible_location)
    for location in range(1, last_accessible_location + 1):
        MemoryBankItemWithAnnotation.show(
            bank,
            location,
            query_device_value(dali, adr, DeviceQueryCommandOpcode.READ_MEMORY),
        )
