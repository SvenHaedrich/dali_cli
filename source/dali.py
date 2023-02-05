from queue import Empty
import sys
import logging
import time

from DALI.forward_frame_16bit import ForwardFrame16Bit
from DALI.address_byte import DALIAddressByte
from DALI.raw_frame import Raw_Frame

import dali_serial
import dali_lunatone
import click


from gear import query as gear_query_cmd

# global data
connection = None
timeout_sec = 0.15


@click.group(name="dali")
@click.version_option("0.0.2")
@click.option(
    "--serial-port",
    envvar="DALI_SERIAL_PORT",
    type=click.Path(),
    help="Serial port used for DALI communication.",
)
@click.option(
    "-l",
    "--lunatone",
    help="Use a Lunatone USB connector for DALI communication.",
    envvar="DALI_LUNATONE",
    is_flag=True,
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
@click.pass_context
def cli(ctx, serial_port, lunatone, debug):
    """
    Command line interface for DALI systems.
    SevenLabs 2023
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    global connection
    if serial_port and not lunatone:
        connection = dali_serial.DALI_Serial(port=serial_port, transparent=True)

    if lunatone and not serial_port:
        connection = dali_lunatone.DALI_Usb()

    if connection == None:
        click.echo("Illegal DALI source settings. Exit now.")
        sys.exit(2)


def simple_level_command(adr, mnemonic):
    address = DALIAddressByte()
    address.arg(adr)
    opcode = ForwardFrame16Bit.opcode(mnemonic)
    command = address.byte << 8 | opcode
    frame = Raw_Frame(length=16, data=command)
    global connection
    connection.write(frame)


@cli.command(name="off", help="Lights off.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def off(adr):
    simple_level_command(adr, "off")


@cli.command(name="up", help="Dim up.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def min(adr):
    simple_level_command(adr, "up")


@cli.command(name="down", help="Dim down.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def min(adr):
    simple_level_command(adr, "down")


@cli.command(name="max", help="Recall maximum.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def max(adr):
    simple_level_command(adr, "recall max level")


@cli.command(name="min", help="Recall minimum.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def min(adr):
    simple_level_command(adr, "recall min level")


@cli.command(name="dapc", help="Direct arc power control (dim level).")
@click.argument("level", type=click.INT)
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def dapc(adr, level):
    if level in range(0x100):
        address = DALIAddressByte(dapc=True)
        address.arg(adr)
        command = address.byte << 8 | level
        frame = Raw_Frame(length=16, data=command)
        connection.write(frame)


@cli.command(name="goto", help="Go to scene.")
@click.argument("scene", type=click.INT)
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def goto(adr, scene):
    address = DALIAddressByte()
    address.arg(adr)
    opcode = ForwardFrame16Bit.opcode(f"GO TO SCENE {scene}")
    command = address.byte << 8 | opcode
    frame = Raw_Frame(length=16, data=command)
    connection.write(frame)


def gear_query_value(adr, opcode):
    connection.start_read()
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    connection.write(cmd_frame)
    try:
        while True:
            frame = connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                connection.close()
                return frame.data
    except Empty:
        connection.close()
        return None


def gear_query_and_display_reply(adr, opcode):
    connection.start_read()
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    connection.write(cmd_frame)
    answer = False
    try:
        while not answer:
            frame = connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                answer = True
                click.echo(f"{frame.data} = 0x{frame.data:02X} = {frame.data:08b}b")
    except Empty:
        if not answer:
            click.echo("timeout - NO")
    connection.close()


def gear_query_multiple(adr, opcode):
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    connection.write(cmd_frame)
    try:
        while True:
            frame = connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                return frame.data
    except Empty:
        return None


@click.group(name="gear", help="Control gear commands.")
def gear():
    pass


def gear_summary_item(adr, caption, command_mnemonic):
    result = gear_query_multiple(adr, ForwardFrame16Bit.opcode(command_mnemonic))
    if not result == None:
        click.echo(f"{caption:.<20}: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo(f"{caption:.<20}: NO - timeout")


@gear.command(name="summary", help="Show status summary.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def gear_summary(adr):
    connection.start_read()
    gear_summary_item(adr, "Status", "QUERY STATUS")
    gear_summary_item(adr, "Operation mode", "QUERY OPERATING MODE")
    gear_summary_item(adr, "Version", "QUERY VERSION NUMBER")
    gear_summary_item(adr, "Actual level", "QUERY ACTUAL LEVEL")
    gear_summary_item(adr, "Power on level", "QUERY POWER ON LEVEL")
    gear_summary_item(adr, "System failure level", "QUERY SYSTEM FAILURE LEVEL")
    gear_summary_item(adr, "Physical minimum", "QUERY PHYSICAL MINIMUM")
    gear_summary_item(adr, "Minimum level", "QUERY MIN LEVEL")
    gear_summary_item(adr, "Maximum level", "QUERY MAX LEVEL")
    gear_summary_item(adr, "Device type", "QUERY DEVICE TYPE")
    gear_summary_item(adr, "DTR0", "QUERY CONTENT DTR0")
    gear_summary_item(adr, "DTR1", "QUERY CONTENT DTR1")
    gear_summary_item(adr, "DTR2", "QUERY CONTENT DTR2")
    random_h = gear_query_multiple(
        adr, ForwardFrame16Bit.opcode("QUERY RANDOM ADDRESS (H)")
    )
    random_m = gear_query_multiple(
        adr, ForwardFrame16Bit.opcode("QUERY RANDOM ADDRESS (M)")
    )
    random_l = gear_query_multiple(
        adr, ForwardFrame16Bit.opcode("QUERY RANDOM ADDRESS (L)")
    )
    random_address = random_h << 16 | random_m << 8 | random_l
    click.echo(
        f"Random address .....: {random_address} = 0x{random_address:06X} = {random_address:024b}b"
    )
    connection.close()


@gear.command(name="list", help="List available short addresses.")
def gear_list(session):
    session.connection.start_read()
    opcode = 0x91
    address = DALIAddressByte()
    address.broadcast()
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    session.connection.write(cmd_frame)
    answer = False
    try:
        while not answer:
            frame = session.connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame:
                answer = True
    except Empty:
        pass
    if answer:
        click.echo("Found control gears:")
        for short_address in range(0x40):
            address.short(short_address)
            command = address.byte << 8 | opcode
            frame = Raw_Frame(length=16, data=command)
            session.connection.write(frame)
            answer = False
            try:
                while not answer:
                    frame = session.connection.read_raw_frame(0.15)
                    if frame.data == cmd_frame.data:
                        continue
                    if frame.length == 8 and frame.data == 0xFF:
                        click.echo(f"A{short_address:02}")
            except Empty:
                pass
    session.connection.close()


@gear.command(name="set", help="Set control gear.")
def gear_set():
    pass

    """ nothing to see here
    """


@gear.command(name="dtr0")
def gear_dtr0():
    pass


@gear.group(name="query", help="Query gear status.")
def gear_query():
    pass


gear_query.add_command(gear_query_cmd.status)
gear_query.add_command(gear_query_cmd.present)
gear_query.add_command(gear_query_cmd.failure)
gear_query.add_command(gear_query_cmd.power)
gear_query.add_command(gear_query_cmd.limit)
gear_query.add_command(gear_query_cmd.reset)
gear_query.add_command(gear_query_cmd.missing)
gear_query.add_command(gear_query_cmd.version)
gear_query.add_command(gear_query_cmd.dtr0)
gear_query.add_command(gear_query_cmd.device_type)
gear_query.add_command(gear_query_cmd.next_device_type)
gear_query.add_command(gear_query_cmd.phm)
gear_query.add_command(gear_query_cmd.power_cycles)
gear_query.add_command(gear_query_cmd.dtr1)
gear_query.add_command(gear_query_cmd.dtr2)
gear_query.add_command(gear_query_cmd.op_mode)
gear_query.add_command(gear_query_cmd.light_source)
gear_query.add_command(gear_query_cmd.actual_level)
gear_query.add_command(gear_query_cmd.min_level)
gear_query.add_command(gear_query_cmd.max_level)
gear_query.add_command(gear_query_cmd.power_level)
gear_query.add_command(gear_query_cmd.failure_level)


@click.group(name="device", help="Control device commands.")
def device():
    pass


@device.command(name="list")
def device_list():
    click.echo("device list")


cli.add_command(device)
cli.add_command(gear)
