import click
import dali

from .opcode import ConfigureCommandOpcode, SpecialCommandOpcode
from .action import write_gear_frame, set_dtr0, gear_send_forward_frame


@click.command(name="clear", help="Clear all short addresses and group settings.")
def clear():
    write_gear_frame(SpecialCommandOpcode.INITIALISE, send_twice=True, block=True)
    set_dtr0(0xFF)
    write_gear_frame(SpecialCommandOpcode.DTR0, opcode_byte=0xFF)
    dali.connection.get(dali.timeout_sec)
    if not dali.connection.data == dali.connection.last_transmit:
        click.echo("transmit DTR0 failed.")
    address = "BC"
    gear_send_forward_frame(address, ConfigureCommandOpcode.SET_SHORT_ADR, True)
    dali.connection.get(dali.timeout_sec)
    dali.connection.get(dali.timeout_sec)
    if not dali.connection.data == dali.connection.last_transmit:
        click.echo("transmit SET SHORT ADDRESS failed.")
    for group in range(dali.MAX_GROUP):
        gear_send_forward_frame(
            address, (ConfigureCommandOpcode.REMOVE_GROUP + group), True
        )
        dali.connection.get(dali.timeout_sec)
        dali.connection.get(dali.timeout_sec)
        if not dali.connection.data == dali.connection.last_transmit:
            click.echo(f"transmit REMOVE GROUP {group} failed.")
    write_gear_frame(SpecialCommandOpcode.TERMINATE)
    dali.connection.close()
