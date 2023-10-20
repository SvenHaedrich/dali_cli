from typeguard import typechecked
import click
import dali

from .action import gear_query_value
from .opcode import QueryCommandOpcode


@typechecked
def gear_summary_item(adr: str, caption: str, opcode: int) -> None:
    result = gear_query_value(adr, opcode, close=False)
    if result is not None:
        click.echo(f"{caption:.<20}: 0x{result:02X} = {result:08b}b = {result}")
    else:
        click.echo(f"{caption:.<20}: NO - timeout")


@click.command(name="summary", help="Show status summary.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@typechecked
def summary(adr: str) -> None:
    gear_summary_item(adr, "Status", QueryCommandOpcode.STATUS)
    gear_summary_item(adr, "Operation mode", QueryCommandOpcode.OPERATING_MODE)
    gear_summary_item(adr, "Version", QueryCommandOpcode.VERSION_NUMBER)
    gear_summary_item(adr, "Actual level", QueryCommandOpcode.ACTUAL_LEVEL)
    gear_summary_item(adr, "Power on level", QueryCommandOpcode.POWER_ON_LEVEL)
    gear_summary_item(
        adr, "System failure level", QueryCommandOpcode.SYSTEM_FAILURE_LEVEL
    )
    gear_summary_item(adr, "Physical minimum", QueryCommandOpcode.PHYSICAL_MINIMUM)
    gear_summary_item(adr, "Minimum level", QueryCommandOpcode.MIN_LEVEL)
    gear_summary_item(adr, "Maximum level", QueryCommandOpcode.MAX_LEVEL)
    gear_summary_item(adr, "Device type", QueryCommandOpcode.DEVICE_TYPE)
    gear_summary_item(adr, "DTR0", QueryCommandOpcode.CONTENT_DTR0)
    gear_summary_item(adr, "DTR1", QueryCommandOpcode.CONTENT_DTR1)
    gear_summary_item(adr, "DTR2", QueryCommandOpcode.CONTENT_DTR2)
    random_h = gear_query_value(adr, QueryCommandOpcode.RANDOM_ADDRESS_H, close=False)
    random_m = gear_query_value(adr, QueryCommandOpcode.RANDOM_ADDRESS_M, close=False)
    random_l = gear_query_value(adr, QueryCommandOpcode.RANDOM_ADDRESS_L, close=False)
    if (random_h is not None) and (random_m is not None) and (random_l is not None):
        random_address = random_h << 16 | random_m << 8 | random_l
        click.echo(
            f"Random address .....: 0x{random_address:06X} = "
            f"{random_address:024b}b = "
            f"{random_address}"
        )
    else:
        click.echo("Random address .....: NO - timeout")
    gear_summary_item(adr, "Groups 0-7", QueryCommandOpcode.GROUPS_0_7)
    gear_summary_item(adr, "Groups 8-15", QueryCommandOpcode.GROUPS_8_15)
    gear_summary_item(adr, "Fade time & rate", QueryCommandOpcode.FADE_TIME_RATE)
    gear_summary_item(adr, "Extended fade time", QueryCommandOpcode.EXTENDED_FADE_TIME)
    for scene in range(dali.MAX_SCENE):
        gear_summary_item(
            adr, f"Scene {scene} level", QueryCommandOpcode.SCENE_LEVEL + scene
        )
