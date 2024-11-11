"""Control gear level command implementations."""

import click
import dali

from .action import gear_send_forward_frame
from .opcode import LevelCommandOpcode
from .address import DaliAddressByte
from ..dali_interface.dali_interface import DaliFrame

gear_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)


@click.command(name="off", help="Lights off.")
@gear_address_option
def off(adr):
    gear_send_forward_frame(adr, LevelCommandOpcode.OFF)
    dali.connection.close()


@click.command(name="up", help="Dim up.")
@gear_address_option
def up(adr):
    gear_send_forward_frame(adr, LevelCommandOpcode.UP)


@click.command(name="down", help="Dim down.")
@gear_address_option
def down(adr):
    gear_send_forward_frame(adr, LevelCommandOpcode.DOWN)


@click.command(name="max", help="Recall maximum.")
@gear_address_option
def max(adr):
    gear_send_forward_frame(adr, LevelCommandOpcode.RECALL_MAX)


@click.command(name="min", help="Recall minimum.")
@gear_address_option
def min(adr):
    gear_send_forward_frame(adr, LevelCommandOpcode.RECALL_MIN)


@click.command(
    name="dapc",
    help="Direct arc power control (dim LEVEL). "
    "LEVEL needs to be between 0 and 255. "
    "Note, that 255 is the MASK value that will not change the actual light level.",
)
@click.argument("level", type=click.INT)
@gear_address_option
def dapc(adr, level):
    if level in range(dali.MAX_VALUE):
        address = DaliAddressByte(dapc=True)
        if address.arg(adr):
            command = address.byte << 8 | level
            dali.connection.transmit(DaliFrame(length=16, data=command))
        else:
            raise click.BadOptionUsage("adr", "invalid address option")
    else:
        raise click.BadParameter("needs to be between 0 and 255.", param_hint="LEVEL")


@click.command(name="goto", help="Go to SCENE. SCENE needs to be between 0 and 15")
@click.argument("scene", type=click.INT)
@gear_address_option
def goto(adr, scene):
    if scene in range(dali.MAX_SCENE):
        gear_send_forward_frame(adr, (LevelCommandOpcode.GOTO_SCENE + scene))
    else:
        raise click.BadParameter("needs to be between 0 and 15.", param_hint="SCENE")
