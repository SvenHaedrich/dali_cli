from queue import Empty
from DALI.forward_frame_16bit import ForwardFrame16Bit
from DALI.address_byte import DALIAddressByte
from DALI.raw_frame import Raw_Frame

import logging
import click
import dali

logger = logging.getLogger(__name__)


def gear_query_value(adr, opcode):
    logging.debug("gear_query_value")
    dali.connection.start_read()
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    dali.connection.write(cmd_frame)
    while True:
        try:
            frame = dali.connection.read_raw_frame(dali.timeout_sec)
        except Empty:
            logging.debug("no frame received")
            frame.data = None
            break
        if frame.data == cmd_frame.data:
            logging.debug("received query command")
            continue
        if frame.length == 8:
            logging.debug("received backward frame")
            break
    dali.connection.close()
    return frame.data


def gear_query_and_display_reply(adr, opcode):
    dali.connection.start_read()
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    dali.connection.write(cmd_frame)
    answer = False
    try:
        while not answer:
            frame = dali.connection.read_raw_frame(dali.timeout_sec)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                answer = True
                click.echo(f"{frame.data} = 0x{frame.data:02X} = {frame.data:08b}b")
    except Empty:
        if not answer:
            click.echo("timeout - NO")
    dali.connection.close()


@click.command(name="status", help="Gear status byte")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def status(adr):
    result = gear_query_value(adr, ForwardFrame16Bit.opcode("QUERY STATUS"))
    logging.debug(f"result is <{result}>")
    if not result == None:
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


@click.command(name="present", help="Control gear present")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def present(adr):
    gear_query_and_display_reply(
        adr, ForwardFrame16Bit.opcode("QUERY CONTROL GEAR PRESENT")
    )


@click.command(name="failure", help="Lamp failure")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def failure(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY LAMP FAILURE"))


@click.command(name="power", help="Gear lamp power on")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def power(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY LAMP POWER ON"))


@click.command(name="limit", help="Limit error")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def limit(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY LIMIT ERROR"))


@click.command(name="reset", help="Reset state")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def reset(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY RESET STATE"))


@click.command(name="short", help="Missing short address")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def missing(adr):
    gear_query_and_display_reply(
        adr, ForwardFrame16Bit.opcode("QUERY MISSING SHORT ADDRESS")
    )


@click.command(name="version", help="Version number")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def version(adr):
    result = gear_query_value(adr, ForwardFrame16Bit.opcode("QUERY VERSION NUMBER"))
    if not result == None:
        click.echo(f"Version: {result} = 0x{result:02X} = {result:08b}b")
        click.echo(f" equals: {(result>>2)}.{(result&0x3)}")
    else:
        click.echo("Status: NO - timeout")


@click.command(name="dtr0", help="Content DTR0")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def dtr0(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY CONTENT DTR0"))


@click.command(name="dt", help="Device type")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def device_type(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY DEVICE TYPE"))


@click.command(name="next", help="Next device type")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def next_device_type(adr):
    gear_query_and_display_reply(
        adr, ForwardFrame16Bit.opcode("QUERY NEXT DEVICE TYPE")
    )


@click.command(name="phm", help="Physical minimum")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def phm(adr):
    gear_query_and_display_reply(
        adr, ForwardFrame16Bit.opcode("QUERY PHYSICAL MINIMUM")
    )


@click.command(name="power_cycle", help="Power cycle seen")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def power_cycles(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY POWER FAILURE"))


@click.command(name="dtr1", help="Content DTR1")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def dtr1(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY CONTENT DTR1"))


@click.command(name="dtr2", help="Content DTR2")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def dtr2(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY CONTENT DTR2"))


@click.command(name="op", help="Operating mode")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def op_mode(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY OPERATING MODE"))


@click.command(name="light", help="Light source type")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def light_source(adr):
    gear_query_and_display_reply(
        adr, ForwardFrame16Bit.opcode("QUERY LIGHT SOURCE TYPE")
    )


@click.command(name="actual", help="Actual level")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def actual_level(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY ACTUAL LEVEL"))


@click.command(name="max", help="Maximum light level")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def max_level(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY MAX LEVEL"))


@click.command(name="min", help="Minimum light level")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def min_level(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY MIN LEVEL"))


@click.command(name="on", help="Power on light level")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def power_level(adr):
    gear_query_and_display_reply(adr, ForwardFrame16Bit.opcode("QUERY POWER ON LEVEL"))


@click.command(name="fail", help="System failure light level")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def failure_level(adr):
    gear_query_and_display_reply(
        adr, ForwardFrame16Bit.opcode("QUERY SYSTEM FAILURE LEVEL")
    )
