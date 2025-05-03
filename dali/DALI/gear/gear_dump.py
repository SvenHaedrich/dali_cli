"""Control gear dump memory bank contents."""

import click

from ..dali_interface.dali_interface import DaliInterface
from ..system.membank_annotation import MemoryBankItemWithAnnotation
from .gear_action import query_gear_value, set_gear_dtr0, set_gear_dtr1
from .gear_opcode import GearQueryCommandOpcode


@click.command(name="dump", help="Dump contents of a memory bank.")
@click.argument("bank", type=click.INT)
@click.pass_obj
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)
def dump(dali: DaliInterface, adr, bank):
    set_gear_dtr1(dali, bank, "BANK")
    set_gear_dtr0(dali, 0, "LOCATION")
    last_accessible_location = query_gear_value(
        dali, adr, GearQueryCommandOpcode.READ_MEMORY
    )
    if last_accessible_location is None:
        click.echo(f"memory bank {bank} not implemented")
        return
    MemoryBankItemWithAnnotation.show(bank, 0, last_accessible_location)
    for location in range(1, last_accessible_location + 1):
        MemoryBankItemWithAnnotation.show(
            bank,
            location,
            query_gear_value(dali, adr, GearQueryCommandOpcode.READ_MEMORY),
        )
