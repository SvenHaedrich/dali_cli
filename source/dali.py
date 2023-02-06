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
from gear import level as level_cmd
from gear import summary as gear_summary_cmd
from gear import list as gear_list_cmd

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


cli.add_command(level_cmd.off)
cli.add_command(level_cmd.up)
cli.add_command(level_cmd.down)
cli.add_command(level_cmd.max)
cli.add_command(level_cmd.min)
cli.add_command(level_cmd.dapc)
cli.add_command(level_cmd.goto)


@cli.group(name="gear", help="Control gear commands.")
def gear():
    pass


gear.add_command(gear_summary_cmd.summary)
gear.add_command(gear_list_cmd.list)


@gear.group(name="set", help="Set control gear.")
def gear_set():
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
