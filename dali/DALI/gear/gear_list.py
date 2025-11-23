"""Control gear list available short addresses."""

import click
from dali_interface import DaliFrame, DaliInterface, DaliStatus

from ..system.constants import DaliFrameLength, DaliMax
from .gear_address import GearAddress
from .gear_opcode import GearQueryCommandOpcode


@click.command(name="list", help="List available short addresses.")
@click.pass_obj
def gear_list(context: DaliInterface) -> None:
    address = GearAddress()
    address.broadcast()
    command = address.byte << 8 | GearQueryCommandOpcode.GEAR_PRESENT
    with context as dali:
        reply = dali.query_reply(DaliFrame(length=DaliFrameLength.GEAR, data=command))
        if reply.status != DaliStatus.TIMEOUT:
            click.echo("Found control gears.")
            for short_address in range(DaliMax.ADR):
                address.arg(f"{short_address:02}")
                command = address.byte << 8 | GearQueryCommandOpcode.GEAR_PRESENT
                reply = dali.query_reply(DaliFrame(length=16, data=command))
                if reply.status != DaliStatus.TIMEOUT:
                    click.echo(message=f"{short_address}\r", nl=False)
                    if reply.length == 8 and reply.data == 0xFF:
                        click.echo(f"G{short_address:02}")
