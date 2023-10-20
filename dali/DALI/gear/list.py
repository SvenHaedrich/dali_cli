import click
import dali

from .opcode import QueryCommandOpcode
from .address import DaliAddressByte
from ..dali_interface.dali_interface import DaliFrame, DaliStatus


@click.command(name="list", help="List available short addresses.")
def list() -> None:
    address = DaliAddressByte()
    address.broadcast()
    command = address.byte << 8 | QueryCommandOpcode.GEAR_PRESENT
    reply = dali.connection.query_reply(DaliFrame(length=16, data=command))
    if reply.status != DaliStatus.TIMEOUT:
        click.echo("Found control gears:")
        for short_address in range(dali.MAX_ADR):
            address.arg(f"{short_address:02}")
            command = address.byte << 8 | QueryCommandOpcode.GEAR_PRESENT
            reply = dali.connection.query_reply(DaliFrame(length=16, data=command))
            if reply.status != DaliStatus.TIMEOUT:
                click.echo(message=f"{short_address}\r", nl=False)
                if reply.length == 8 and reply.data == 0xFF:
                    click.echo(f"G{short_address:02}")
