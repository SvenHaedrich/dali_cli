import click
import dali

from .opcode import QueryCommandOpcode
from .action import gear_query_value, gear_query_and_display_reply


gear_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (0..63) or group address (G0..G15).",
)


@click.command(name="status", help="Gear status byte")
@gear_address_option
def status(adr):
    dali.connection.start_receive()
    result = gear_query_value(adr, QueryCommandOpcode.STATUS)
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
    dali.connection.close()


@click.command(name="present", help="Control gear present")
@gear_address_option
def present(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.GEAR_PRESENT)


@click.command(name="failure", help="Lamp failure")
@gear_address_option
def failure(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.LAMP_FAILURE)


@click.command(name="power", help="Gear lamp power on")
@gear_address_option
def power(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.LAMP_POWER_ON)


@click.command(name="limit", help="Limit error")
@gear_address_option
def limit(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.LIMIT_ERROR)


@click.command(name="reset", help="Reset state")
@gear_address_option
def reset(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.RESET_STATE)


@click.command(name="short", help="Missing short address")
@gear_address_option
def missing(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.MISSING_SHORT_ADDRESS)


@click.command(name="version", help="Version number")
@gear_address_option
def version(adr):
    dali.connection.start_receive()
    result = gear_query_value(adr, QueryCommandOpcode.VERSION_NUMBER)
    if result is not None:
        click.echo(f"Version: {result} = 0x{result:02X} = {result:08b}b")
        click.echo(f" equals: {(result>>2)}.{(result&0x3)}")
    else:
        click.echo("timeout - NO")
    dali.connection.close()


@click.command(name="dtr0", help="Content DTR0")
@gear_address_option
def dtr0(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.CONTENT_DTR0)


@click.command(name="dt", help="Device type")
@gear_address_option
def device_type(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.DEVICE_TYPE)


@click.command(name="next", help="Next device type")
@gear_address_option
def next_device_type(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.NEXT_DEVICE_TYPE)


@click.command(name="phm", help="Physical minimum")
@gear_address_option
def phm(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.PHYSICAL_MINIMUM)


@click.command(name="power_cycle", help="Power cycle seen")
@gear_address_option
def power_cycles(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.POWER_FAILURE)


@click.command(name="dtr1", help="Content DTR1")
@gear_address_option
def dtr1(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.CONTENT_DTR1)


@click.command(name="dtr2", help="Content DTR2")
@gear_address_option
def dtr2(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.CONTENT_DTR2)


@click.command(name="op", help="Operating mode")
@gear_address_option
def op_mode(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.OPERATING_MODE)


@click.command(name="light", help="Light source type")
@gear_address_option
def light_source(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.LIGHT_SOURCE_TYPE)


@click.command(name="actual", help="Actual level")
@gear_address_option
def actual_level(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.ACTUAL_LEVEL)


@click.command(name="max", help="Maximum light level")
@gear_address_option
def max_level(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.MAX_LEVEL)


@click.command(name="min", help="Minimum light level")
@gear_address_option
def min_level(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.MIN_LEVEL)


@click.command(name="on", help="Power on light level")
@gear_address_option
def power_level(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.POWER_ON_LEVEL)


@click.command(name="fail", help="System failure light level")
@gear_address_option
def failure_level(adr):
    gear_query_and_display_reply(adr, QueryCommandOpcode.SYSTEM_FAILURE_LEVEL)


@click.command(name="fade", help="Fade rate and fade time")
@gear_address_option
def fade(adr):
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
        "127 stes/s",
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
    dali.connection.start_receive()
    result = gear_query_value(adr, QueryCommandOpcode.FADE_TIME_RATE)
    if result is not None:
        click.echo(f"Result: {result} = 0x{result:02X} = {result:08b}b")
        click.echo(f" fade time: {fade_time[(result >> 4) &0xF]}")
        click.echo(f" fade rate: {fade_rate[(result & 0xF)]}")
    else:
        click.echo("timeout - NO")
    dali.connection.close()
