"""Control gear list available short addresses."""

import click

from ..dali_interface.dali_interface import DaliFrame, DaliStatus
from ..system.constants import DaliMax
from .address import DaliAddressByte
from .gear_opcode import GearQueryCommandOpcode


@click.command(name="list", help="List available short addresses.")
def list() -> None:
    address = DaliAddressByte()
    address.broadcast()
    command = address.byte << 8 | GearQueryCommandOpcode.GEAR_PRESENT
    reply = dali.connection.query_reply(DaliFrame(length=16, data=command))
    if reply.status != DaliStatus.TIMEOUT:
        click.echo("Found control gears.")
        for short_address in range(DaliMax.ADR):
            address.arg(f"{short_address:02}")
            command = address.byte << 8 | GearQueryCommandOpcode.GEAR_PRESENT
            reply = dali.connection.query_reply(DaliFrame(length=16, data=command))
            if reply.status != DaliStatus.TIMEOUT:
                click.echo(message=f"{short_address}\r", nl=False)
                if reply.length == 8 and reply.data == 0xFF:
                    click.echo(f"G{short_address:02}")
