"""Command sequence to clear short addresses and group settings."""

import click
import dali

from .action import gear_send_forward_frame, set_dtr0, write_gear_frame 
from .gear_opcode import GearConfigureCommandOpcode, GearSpecialCommandOpcode


@click.command(name="clear", help="Clear all short addresses and group settings.")
def clear():
    write_gear_frame(GearSpecialCommandOpcode.INITIALISE, send_twice=True, block=True)
    set_dtr0(0xFF)
    write_gear_frame(GearSpecialCommandOpcode.DTR0, opcode_byte=0xFF)
    dali.connection.get(dali.timeout_sec)
    if not dali.connection.data == dali.connection.last_transmit:
        click.echo("transmit DTR0 failed.")
    address = "BC"
    gear_send_forward_frame(address, GearConfigureCommandOpcode.SET_SHORT_ADR, True)
    dali.connection.get(dali.timeout_sec)
    dali.connection.get(dali.timeout_sec)
    if not dali.connection.data == dali.connection.last_transmit:
        click.echo("transmit SET SHORT ADDRESS failed.")
    for group in range(DaliMax.GROUP):
        gear_send_forward_frame(
            address, (GearConfigureCommandOpcode.REMOVE_GROUP + group), True
        )
        dali.connection.get(dali.timeout_sec)
        dali.connection.get(dali.timeout_sec)
        if not dali.connection.data == dali.connection.last_transmit:
            click.echo(f"transmit REMOVE GROUP {group} failed.")
    write_gear_frame(GearSpecialCommandOpcode.TERMINATE)
    dali.connection.close()
