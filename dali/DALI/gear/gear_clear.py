"""Command sequence to clear short addresses and group settings."""

import click
from dali_interface import DaliInterface

from ..system.constants import DaliMax, DaliTimeout
from .gear_action import (
    gear_send_forward_frame,
    set_gear_dtr0,
    write_gear_frame,
    write_gear_frame_and_wait,
)
from .gear_opcode import GearConfigureCommandOpcode, GearSpecialCommandOpcode


@click.command(name="clear", help="Clear all short addresses and group settings.")
@click.pass_obj
def clear(dali: DaliInterface):
    write_gear_frame(dali, GearSpecialCommandOpcode.INITIALISE, send_twice=True)
    set_gear_dtr0(dali, 0xFF)
    write_gear_frame_and_wait(dali, GearSpecialCommandOpcode.DTR0, opcode_byte=0xFF)
    address = "BC"
    gear_send_forward_frame(
        dali, address, GearConfigureCommandOpcode.SET_SHORT_ADDRESS, True
    )
    dali.get(DaliTimeout.DEFAULT.value)
    dali.get(DaliTimeout.DEFAULT.value)
    if not dali.data == dali.last_transmit:
        click.echo("transmit SET SHORT ADDRESS failed.")
    for group in range(DaliMax.GROUP):
        gear_send_forward_frame(
            dali, address, (GearConfigureCommandOpcode.REMOVE_GROUP + group), True
        )
        dali.get(DaliTimeout.DEFAULT.value)
        dali.get(DaliTimeout.DEFAULT.value)
        if not dali.data == dali.last_transmit:
            click.echo(f"transmit REMOVE GROUP {group} failed.")
        write_gear_frame(dali, GearSpecialCommandOpcode.TERMINATE)
