"""Command sequence to clear short addresses and group settings."""

import click
from dali_interface import DaliInterface

from ..system.constants import DaliMax, DaliTimeout
from .gear_action import (
    set_gear_dtr0,
    write_gear_frame,
    write_gear_frame_and_wait,
)
from .gear_address import GearAddress
from .gear_opcode import GearConfigureCommandOpcode, GearSpecialCommandOpcode


@click.command(name="clear", help="Clear all short addresses and group settings.")
@click.pass_obj
def clear(dali: DaliInterface):
    write_gear_frame(dali, GearSpecialCommandOpcode.INITIALISE, send_twice=True)
    set_gear_dtr0(dali, 0xFF)
    address = GearAddress()
    address.arg("BC")
    write_gear_frame_and_wait(dali, address.byte, GearConfigureCommandOpcode.SET_SHORT_ADDRESS, send_twice=True)
    for group in range(DaliMax.GEAR_GROUP):
        write_gear_frame_and_wait(dali, address.byte, (GearConfigureCommandOpcode.REMOVE_GROUP + group), True)
    write_gear_frame(dali, GearSpecialCommandOpcode.TERMINATE)
