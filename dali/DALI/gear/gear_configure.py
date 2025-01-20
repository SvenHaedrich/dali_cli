"""Control gear configure command implementations."""

import click

from ..system.constants import DaliMax
from .gear_action import gear_send_forward_frame, set_dtr0
from .gear_opcode import GearConfigureCommandOpcode

gear_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)


@click.command(
    name="reset", help="Reset all control gear variables to their reset value."
)
@click.pass_obj
@gear_address_option
def reset(dali, adr):
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.RESET, True)


@click.command(name="actual", help="Store the actualLevel into DTR0.")
@click.pass_obj
@gear_address_option
def actual(dali, adr):
    gear_send_forward_frame(
        dali, adr, GearConfigureCommandOpcode.STORE_ACTUAL_LEVEL, True
    )


@click.command(name="op", help="Set operating mode.")
@click.pass_obj
@gear_address_option
@click.argument("mode", type=click.INT)
def op(dali, adr, mode):
    set_dtr0(dali, mode, "MODE")
    gear_send_forward_frame(
        dali, adr, GearConfigureCommandOpcode.SET_OPERATION_MODE, True
    )


@click.command(name="reset_mem", help="Reset memory bank to reset value.")
@click.pass_obj
@gear_address_option
@click.argument("bank", type=click.INT)
def reset_mem(dali, adr, bank):
    set_dtr0(dali, bank, "BANK")
    gear_send_forward_frame(
        dali, adr, GearConfigureCommandOpcode.RESET_MEMORY_BANK, True
    )


@click.command(name="id", help="Identify device.")
@click.pass_obj
@gear_address_option
def identify(dali, adr):
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.IDENTIFY_GEAR, True)


@click.command(name="max", help="Set maximum level.")
@click.pass_obj
@gear_address_option
@click.argument("level", type=click.INT)
def max_level(dali, adr, level):
    set_dtr0(dali, level, "LEVEL")
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.SET_MAX_LEVEL, True)


@click.command(name="min", help="Set minimum level.")
@click.pass_obj
@gear_address_option
@click.argument("level", type=click.INT)
def min_level(dali, adr, level):
    set_dtr0(dali, level, "LEVEL")
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.SET_MIN_LEVEL, True)


@click.command(name="fail", help="Set system failure level.")
@click.pass_obj
@gear_address_option
@click.argument("level", type=click.INT)
def fail(dali, adr, level):
    set_dtr0(dali, level, "LEVEL")
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.SET_FAIL_LEVEL, True)


@click.command(name="on", help="Set power on level.")
@click.pass_obj
@gear_address_option
@click.argument("level", type=click.INT)
def on(dali, adr, level):
    set_dtr0(dali, level, "LEVEL")
    gear_send_forward_frame(
        dali, adr, GearConfigureCommandOpcode.SET_POWER_ON_LEVEL, True
    )


@click.command(name="time", help="Set fade time.")
@gear_address_option
@click.pass_obj
@click.argument("value", type=click.INT)
def time(dali, adr, value):
    set_dtr0(dali, value, "VALUE")
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.SET_FADE_TIME, True)


@click.command(name="rate", help="Set fade rate.")
@gear_address_option
@click.pass_obj
@click.argument("value", type=click.INT)
def rate(dali, adr, value):
    set_dtr0(dali, value, "VALUE")
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.SET_FADE_RATE, True)


@click.command(name="ext", help="Set extended fade time.")
@gear_address_option
@click.pass_obj
@click.argument("value", type=click.INT)
def ext(dali, adr, value):
    set_dtr0(dali, value, "VALUE")
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.SET_EXT_FADE, True)


@click.command(
    name="scene",
    help="Set scene NUMBER to LEVEL. "
    "Setting LEVEL to MASK (255) effectively removes the gear as member from the scene",
)
@gear_address_option
@click.argument("number", type=click.INT)
@click.argument("level", type=click.INT)
@click.pass_obj
def scene(dali, adr, number, level):
    if 0 <= number < DaliMax.SCENE:
        set_dtr0(dali, level, "LEVEL")
        gear_send_forward_frame(
            dali, adr, (GearConfigureCommandOpcode.SET_SCENE + number), True
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.SCENE-1}", param_hint="NUMBER"
        )


@click.command(name="remove", help="Remove from scene.")
@click.pass_obj
@gear_address_option
@click.argument("number", type=click.INT)
def remove(dali, adr, number):
    if 0 <= number < DaliMax.SCENE:
        gear_send_forward_frame(
            dali, adr, (GearConfigureCommandOpcode.REMOVE_SCENE + number), True
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.SCENE-1}", param_hint="NUMBER"
        )


@click.command(name="add", help="Add to group.")
@click.pass_obj
@gear_address_option
@click.argument("group", type=click.INT)
def add(dali, adr, group):
    if 0 <= group < DaliMax.GEAR_GROUP:
        gear_send_forward_frame(
            dali, adr, (GearConfigureCommandOpcode.ADD_GROUP + group), True
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.GEAR_GROUP-1}", param_hint="NUMBER"
        )


@click.command(name="ungroup", help="Remove from group.")
@click.pass_obj
@gear_address_option
@click.argument("group", type=click.INT)
def ungroup(dali, adr, group):
    if 0 <= group < DaliMax.GEAR_GROUP:
        gear_send_forward_frame(
            dali, adr, (GearConfigureCommandOpcode.REMOVE_GROUP + group), True
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.GEAR_GROUP-1}", param_hint="NUMBER"
        )


@click.command(name="short", help="Set short address to ADDRESS.")
@click.pass_obj
@gear_address_option
@click.argument("address", type=click.INT)
def short(dali, adr, address):
    if 0 <= address < DaliMax.ADR:
        address = (address * 2) + 1
        set_dtr0(dali, address, "ADDRESS")
        gear_send_forward_frame(
            dali, adr, GearConfigureCommandOpcode.SET_SHORT_ADR, True
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.ADR-1}", param_hint="ADDRESS"
        )


@click.command(name="enable", help="Enable write access.")
@click.pass_obj
@gear_address_option
def enable(dali, adr):
    gear_send_forward_frame(dali, adr, GearConfigureCommandOpcode.ENABLE_WRITE, True)
