"""Control gear level command implementations."""

import click

from ..dali_interface.dali_interface import DaliFrame
from ..system.constants import DaliMax
from .gear_action import gear_send_forward_frame
from .gear_address import DaliAddressByte
from .gear_opcode import GearLevelCommandOpcode

gear_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)


@click.command(name="off", help="Lights off.")
@click.pass_obj
@gear_address_option
def off(dali, adr):
    gear_send_forward_frame(dali, adr, GearLevelCommandOpcode.OFF)


@click.command(name="up", help="Dim up.")
@click.pass_obj
@gear_address_option
def up(dali, adr):
    gear_send_forward_frame(dali, adr, GearLevelCommandOpcode.UP)


@click.command(name="down", help="Dim down.")
@click.pass_obj
@gear_address_option
def down(dali, adr):
    gear_send_forward_frame(dali, adr, GearLevelCommandOpcode.DOWN)


@click.command(name="max", help="Recall maximum.")
@click.pass_obj
@gear_address_option
def max_level(dali, adr):
    gear_send_forward_frame(dali, adr, GearLevelCommandOpcode.RECALL_MAX)


@click.command(name="min", help="Recall minimum.")
@click.pass_obj
@gear_address_option
def min_level(dali, adr):
    gear_send_forward_frame(dali, adr, GearLevelCommandOpcode.RECALL_MIN)


@click.command(
    name="dapc",
    help="Direct arc power control (dim LEVEL). "
    "LEVEL needs to be between 0 and 255. "
    "Note, that 255 is the MASK value that will not change the actual light level.",
)
@click.argument("level", type=click.INT)
@click.pass_obj
@gear_address_option
def dapc(dali, adr, level):
    if level in range(DaliMax.VALUE):
        address = DaliAddressByte(dapc=True)
        if address.arg(adr):
            command = address.byte << 8 | level
            dali.transmit(DaliFrame(length=16, data=command))
        else:
            raise click.BadOptionUsage("adr", "invalid address option")
    else:
        raise click.BadParameter("needs to be between 0 and 255.", param_hint="LEVEL")


@click.command(name="goto", help="Go to SCENE. SCENE needs to be between 0 and 15")
@click.argument("scene", type=click.INT)
@click.pass_obj
@gear_address_option
def goto(dali, adr, scene):
    if scene in range(DaliMax.SCENE):
        gear_send_forward_frame(dali, adr, (GearLevelCommandOpcode.GOTO_SCENE + scene))
    else:
        raise click.BadParameter("needs to be between 0 and 15.", param_hint="SCENE")
