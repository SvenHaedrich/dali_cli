"""Control gear query command implementations."""

import click

from ..dali_interface.dali_interface import DaliInterface
from .gear_action import query_gear_and_display_reply, query_gear_value
from .gear_opcode import GearQueryCommandOpcode

gear_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)


@click.command(name="status", help="Query control gear status byte.")
@click.pass_obj
@gear_address_option
def status(dali: DaliInterface, adr):
    result = query_gear_value(dali, adr, GearQueryCommandOpcode.STATUS)
    if result is not None:
        click.echo(f"status: {result} = 0x{result:02X} = {result:08b}b")
        click.echo("bit : description")
        click.echo(f"  {(result >> 0 & 0x01)} : controlGearFailure")
        click.echo(f"  {(result >> 1 & 0x01)} : lampFailure")
        click.echo(f"  {(result >> 2 & 0x01)} : lampOn")
        click.echo(f"  {(result >> 3 & 0x01)} : limitError")
        click.echo(f"  {(result >> 4 & 0x01)} : fadeRunning")
        click.echo(f"  {(result >> 5 & 0x01)} : resetState")
        click.echo(f"  {(result >> 6 & 0x01)} : shortAddress is MASK")
        click.echo(f"  {(result >> 7 & 0x01)} : powerCycleSeen")
    else:
        click.echo("timeout - NO")


@click.command(name="present", help="Control gear present.")
@click.pass_obj
@gear_address_option
def present(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.GEAR_PRESENT)


@click.command(name="failure", help="Lamp failure.")
@click.pass_obj
@gear_address_option
def failure(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.LAMP_FAILURE)


@click.command(name="power", help="Gear lamp power on.")
@click.pass_obj
@gear_address_option
def power(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.LAMP_POWER_ON)


@click.command(name="limit", help="Limit error.")
@click.pass_obj
@gear_address_option
def limit(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.LIMIT_ERROR)


@click.command(name="reset", help="Reset state.")
@click.pass_obj
@gear_address_option
def reset(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.RESET_STATE)


@click.command(name="missing", help="Missing short address.")
@click.pass_obj
@gear_address_option
def missing(dali: DaliInterface, adr):
    query_gear_and_display_reply(
        dali, adr, GearQueryCommandOpcode.MISSING_SHORT_ADDRESS
    )


@click.command(name="version", help="Version number.")
@click.pass_obj
@gear_address_option
def version(dali: DaliInterface, adr):
    result = query_gear_value(dali, adr, GearQueryCommandOpcode.VERSION_NUMBER)
    if result is not None:
        click.echo(f"Version: {result} = 0x{result:02X} = {result:08b}b")
        click.echo(f" equals: {(result>>2)}.{(result&0x3)}")
    else:
        click.echo("timeout - NO")


@click.command(name="dtr0", help="Content of DTR0.")
@click.pass_obj
@gear_address_option
def dtr0(context: DaliInterface, adr):
    query_gear_and_display_reply(context, adr, GearQueryCommandOpcode.CONTENT_DTR0)


@click.command(name="dt", help="Device type.")
@click.pass_obj
@gear_address_option
def device_type(dali, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.DEVICE_TYPE)


@click.command(name="next", help="Next device type.")
@click.pass_obj
@gear_address_option
def next_device_type(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.NEXT_DEVICE_TYPE)


@click.command(name="phm", help="Physical minimum.")
@click.pass_obj
@gear_address_option
def phm(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.PHYSICAL_MINIMUM)


@click.command(name="power_cycle", help="Power cycle seen.")
@click.pass_obj
@gear_address_option
def power_cycles(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.POWER_FAILURE)


@click.command(name="dtr1", help="Content DTR1.")
@click.pass_obj
@gear_address_option
def dtr1(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.CONTENT_DTR1)


@click.command(name="dtr2", help="Content DTR2.")
@click.pass_obj
@gear_address_option
def dtr2(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.CONTENT_DTR2)


@click.command(name="op", help="Operating mode.")
@click.pass_obj
@gear_address_option
def op_mode(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.OPERATING_MODE)


@click.command(name="light", help="Light source type.")
@click.pass_obj
@gear_address_option
def light_source(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.LIGHT_SOURCE_TYPE)


@click.command(name="actual", help="Actual level.")
@click.pass_obj
@gear_address_option
def actual_level(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.ACTUAL_LEVEL)


@click.command(name="max", help="Maximum light level.")
@click.pass_obj
@gear_address_option
def max_level(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.MAX_LEVEL)


@click.command(name="min", help="Minimum light level.")
@click.pass_obj
@gear_address_option
def min_level(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.MIN_LEVEL)


@click.command(name="on", help="Power on light level.")
@click.pass_obj
@gear_address_option
def power_level(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.POWER_ON_LEVEL)


@click.command(name="fail", help="System failure light level.")
@click.pass_obj
@gear_address_option
def failure_level(dali: DaliInterface, adr):
    query_gear_and_display_reply(dali, adr, GearQueryCommandOpcode.SYSTEM_FAILURE_LEVEL)


@click.command(name="fade", help="Fade rate and fade time.")
@click.pass_obj
@gear_address_option
def fade(dali: DaliInterface, adr):
    fade_time = (
        "use extended fade time",
        "0.7 s",
        "1.0 s",
        "1.4 s",
        "2.0 s",
        "2.8 s",
        "4.0 s",
        "5.7 s",
        "8.0 s",
        "11.3 s",
        "16.0 s",
        "22.6 s",
        "32.0 s",
        "45.3 s",
        "64 s",
        "90.5 s",
    )
    fade_rate = (
        "1 step/s",
        "358 steps/s",
        "253 steps/s",
        "179 steps/s",
        "127 steps/s",
        "89.4 steps/s",
        "63.3 steps/s",
        "44.7 steps/s",
        "31.6 steps/s",
        "22.4 steps/s",
        "15.8 steps/s",
        "11.2 steps/s",
        "7.9 steps/s",
        "5.6 steps/s",
        "4.0 steps/s",
        "2.8 steps/s",
    )
    result = query_gear_value(dali, adr, GearQueryCommandOpcode.FADE_TIME_RATE)
    if result is not None:
        click.echo(f"Result: {result} = 0x{result:02X} = {result:08b}b")
        click.echo(f" fade time: {fade_time[(result >> 4) &0xF]}")
        click.echo(f" fade rate: {fade_rate[(result & 0xF)]}")
    else:
        click.echo("timeout - NO")
