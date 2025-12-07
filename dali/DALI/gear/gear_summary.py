"""Control gear setting summary."""

import click
from dali_interface import DaliInterface
from typeguard import typechecked

from ..system.constants import DaliMax
from .gear_action import query_gear_value
from .gear_opcode import GearQueryCommandOpcode


@typechecked
def gear_summary_item(dali: DaliInterface, adr: str, caption: str, opcode: int) -> None:
    result = query_gear_value(dali, adr, opcode)
    if result is not None:
        click.echo(f"{caption:.<20}: 0x{result:02X} = {result:08b}b = {result}")
    else:
        click.echo(f"{caption:.<20}: NO - timeout")


@click.command(name="summary", help="Show status summary.")
@click.pass_obj
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@typechecked
def summary(dali: DaliInterface, adr: str) -> None:
    gear_summary_item(dali, adr, "Status", GearQueryCommandOpcode.STATUS)
    gear_summary_item(dali, adr, "Operation mode", GearQueryCommandOpcode.OPERATING_MODE)
    gear_summary_item(dali, adr, "Version", GearQueryCommandOpcode.VERSION_NUMBER)
    gear_summary_item(dali, adr, "Actual level", GearQueryCommandOpcode.ACTUAL_LEVEL)
    gear_summary_item(dali, adr, "Power on level", GearQueryCommandOpcode.POWER_ON_LEVEL)
    gear_summary_item(dali, adr, "System failure level", GearQueryCommandOpcode.SYSTEM_FAILURE_LEVEL)
    gear_summary_item(dali, adr, "Physical minimum", GearQueryCommandOpcode.PHYSICAL_MINIMUM)
    gear_summary_item(dali, adr, "Minimum level", GearQueryCommandOpcode.MIN_LEVEL)
    gear_summary_item(dali, adr, "Maximum level", GearQueryCommandOpcode.MAX_LEVEL)
    gear_summary_item(dali, adr, "Device type", GearQueryCommandOpcode.DEVICE_TYPE)
    gear_summary_item(dali, adr, "DTR0", GearQueryCommandOpcode.CONTENT_DTR0)
    gear_summary_item(dali, adr, "DTR1", GearQueryCommandOpcode.CONTENT_DTR1)
    gear_summary_item(dali, adr, "DTR2", GearQueryCommandOpcode.CONTENT_DTR2)
    random_h = query_gear_value(dali, adr, GearQueryCommandOpcode.RANDOM_ADDRESS_H)
    random_m = query_gear_value(dali, adr, GearQueryCommandOpcode.RANDOM_ADDRESS_M)
    random_l = query_gear_value(dali, adr, GearQueryCommandOpcode.RANDOM_ADDRESS_L)
    if (random_h is not None) and (random_m is not None) and (random_l is not None):
        random_address = random_h << 16 | random_m << 8 | random_l
        click.echo(f"Random address .....: 0x{random_address:06X} = " f"{random_address:024b}b = " f"{random_address}")
    else:
        click.echo("Random address .....: NO - timeout")
    gear_summary_item(dali, adr, "Groups 0-7", GearQueryCommandOpcode.GROUPS_0_7)
    gear_summary_item(dali, adr, "Groups 8-15", GearQueryCommandOpcode.GROUPS_8_15)
    gear_summary_item(dali, adr, "Fade time & rate", GearQueryCommandOpcode.FADE_TIME_RATE)
    gear_summary_item(dali, adr, "Extended fade time", GearQueryCommandOpcode.EXTENDED_FADE_TIME)
    for scene in range(DaliMax.SCENE):
        gear_summary_item(
            dali,
            adr,
            f"Scene {scene} level",
            GearQueryCommandOpcode.SCENE_LEVEL + scene,
        )
