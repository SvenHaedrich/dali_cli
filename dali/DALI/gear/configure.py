"""Control gear configure command implementations."""

import click

from ..system.constants import DaliMax
from .action import gear_send_forward_frame, set_dtr0
from .gear_opcode import GearConfigureCommandOpcode

gear_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)


@click.command(
    name="reset", help="Reset all control gear variables to their reset value."
)
@gear_address_option
def reset(adr):
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.RESET, True)


@click.command(name="actual", help="Store the actualLevel into DTR0.")
@gear_address_option
def actual(adr):
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.STORE_ACTUAL_LEVEL, True)


@click.command(name="op", help="Set operating mode.")
@gear_address_option
@click.argument("mode", type=click.INT)
def op(adr, mode):
    set_dtr0(mode, "MODE")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_OPERATION_MODE, True)
    dali.connection.close()


@click.command(name="reset_mem", help="Reset memory bank to reset value.")
@gear_address_option
@click.argument("bank", type=click.INT)
def reset_mem(adr, bank):
    set_dtr0(bank, "BANK")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.RESET_MEMORY_BANK, True)


@click.command(name="id", help="Identify device.")
@gear_address_option
def id(adr):
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.IDENTIFY_GEAR, True)


@click.command(name="max", help="Set maximum level.")
@gear_address_option
@click.argument("level", type=click.INT)
def max(adr, level):
    set_dtr0(level, "LEVEL")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_MAX_LEVEL, True)


@click.command(name="min", help="Set minimum level.")
@gear_address_option
@click.argument("level", type=click.INT)
def min(adr, level):
    set_dtr0(level, "LEVEL")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_MIN_LEVEL, True)


@click.command(name="fail", help="Set system failure level.")
@gear_address_option
@click.argument("level", type=click.INT)
def fail(adr, level):
    set_dtr0(level, "LEVEL")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_FAIL_LEVEL, True)


@click.command(name="on", help="Set power on level.")
@gear_address_option
@click.argument("level", type=click.INT)
def on(adr, level):
    set_dtr0(level, "LEVEL")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_POWER_ON_LEVEL, True)


@click.command(name="time", help="Set fade time.")
@gear_address_option
@click.argument("value", type=click.INT)
def time(adr, value):
    set_dtr0(value, "VALUE")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_FADE_TIME, True)


@click.command(name="rate", help="Set fade rate.")
@gear_address_option
@click.argument("value", type=click.INT)
def rate(adr, value):
    set_dtr0(value, "VALUE")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_FADE_RATE, True)


@click.command(name="ext", help="Set extended fade time.")
@gear_address_option
@click.argument("value", type=click.INT)
def ext(adr, value):
    set_dtr0(value, "VALUE")
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_EXT_FADE, True)


@click.command(
    name="scene",
    help="Set scene NUMBER to LEVEL. "
    "Setting LEVEL to MASK (255) effectively removes the gear as member from the scene",
)
@gear_address_option
@click.argument("number", type=click.INT)
@click.argument("level", type=click.INT)
def scene(adr, number, level):
    if number in range(0x10):
        set_dtr0(level, "LEVEL")
        gear_send_forward_frame(
            adr, (GearConfigureCommandOpcode.SET_SCENE + number), True
        )
    else:
        raise click.BadParameter("needs to be between 0 and 15", param_hint="NUMBER")


@click.command(name="remove", help="Remove from scene.")
@gear_address_option
@click.argument("number", type=click.INT)
def remove(adr, number):
    if number in range(0x10):
        gear_send_forward_frame(
            adr, (GearConfigureCommandOpcode.REMOVE_SCENE + number), True
        )
    else:
        raise click.BadParameter("needs to be between 0 and 15", param_hint="NUMBER")


@click.command(name="add", help="Add to group.")
@gear_address_option
@click.argument("group", type=click.INT)
def add(adr, group):
    if group in range(0x10):
        gear_send_forward_frame(
            adr, (GearConfigureCommandOpcode.ADD_GROUP + group), True
        )
    else:
        raise click.BadParameter("needs to be between 0 and 15", param_hint="GROUP")


@click.command(name="ungroup", help="Remove from group.")
@gear_address_option
@click.argument("group", type=click.INT)
def ungroup(adr, group):
    if group in range(0x10):
        gear_send_forward_frame(
            adr, (GearConfigureCommandOpcode.REMOVE_GROUP + group), True
        )
    else:
        raise click.BadParameter("needs to be between 0 and 15", param_hint="GROUP")


@click.command(name="short", help="Set short address to ADDRESS.")
@gear_address_option
@click.argument("address", type=click.INT)
def short(adr, address):
    if 0 <= address < DaliMax.ADR:
        address = (address * 2) + 1
        set_dtr0(address, "ADDRESS")
        gear_send_forward_frame(adr, GearConfigureCommandOpcode.SET_SHORT_ADR, True)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.ADR-1}", param_hint="ADDRESS"
        )


@click.command(name="enable", help="Enable write access.")
@gear_address_option
def enable(adr):
    gear_send_forward_frame(adr, GearConfigureCommandOpcode.ENABLE_WRITE, True)
