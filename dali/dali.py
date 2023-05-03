import logging
import click

from DALI.connection import mock as connection_mock
from DALI.connection import serial as connection_serial
from DALI.connection import hid as connection_hid


from DALI.gear import query as gear_query_cmd
from DALI.gear import level as level_cmd
from DALI.gear import summary as gear_summary_cmd
from DALI.gear import list as gear_list_cmd
from DALI.gear import configure as gear_conf_cmd
from DALI.gear import special as gear_special_cmd

# global data
connection = None
timeout_sec = 0.2

# global const
MAX_GROUP = 0x10
MAX_SCENE = 0x10
MAX_VALUE = 0x100
MAX_ADR = 0x40


@click.group(name="dali")
@click.version_option("0.0.7")
@click.option(
    "--serial-port",
    envvar="DALI_SERIAL_PORT",
    show_envvar=True,
    type=click.Path(),
    help="Serial port used for DALI communication.",
)
@click.option(
    "--hid",
    help="Use a HID class USB connector for DALI communication.",
    envvar="DALI_HID_USB",
    show_envvar=True,
    is_flag=True,
)
@click.option(
    "--mock",
    help="Mock DALI interface for testing.",
    hidden=True,
    is_flag=True,
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
@click.pass_context
def cli(ctx, serial_port, hid, mock, debug):
    """
    Command line interface for DALI systems.
    SevenLabs 2023
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    global connection
    try:
        if serial_port and not hid and not mock:
            connection = connection_serial.DaliSerial(port=serial_port)

        if hid and not serial_port and not mock:
            connection = connection_hid.DaliUsb()

        if mock and not serial_port and not hid:
            connection = connection_mock.DaliMock()

        if connection is None:
            raise click.BadArgumentUsage("invalid connection configuration.")
    except:
        raise click.BadArgumentUsage("can not open connection.")


cli.add_command(level_cmd.off)
cli.add_command(level_cmd.up)
cli.add_command(level_cmd.down)
cli.add_command(level_cmd.max)
cli.add_command(level_cmd.min)
cli.add_command(level_cmd.dapc)
cli.add_command(level_cmd.goto)


#
# ---- gear commands
@cli.group(name="gear", help="Control gear commands.")
def gear():
    pass


gear.add_command(gear_summary_cmd.summary)
gear.add_command(gear_list_cmd.list)

# ---- configure commands
gear.add_command(gear_conf_cmd.reset)
gear.add_command(gear_conf_cmd.actual)
gear.add_command(gear_conf_cmd.op)
gear.add_command(gear_conf_cmd.reset_mem)
gear.add_command(gear_conf_cmd.id)
gear.add_command(gear_conf_cmd.max)
gear.add_command(gear_conf_cmd.min)
gear.add_command(gear_conf_cmd.fail)
gear.add_command(gear_conf_cmd.on)
gear.add_command(gear_conf_cmd.time)
gear.add_command(gear_conf_cmd.rate)
gear.add_command(gear_conf_cmd.ext)
gear.add_command(gear_conf_cmd.scene)
gear.add_command(gear_conf_cmd.remove)
gear.add_command(gear_conf_cmd.add)
gear.add_command(gear_conf_cmd.ungroup)
gear.add_command(gear_conf_cmd.short)
gear.add_command(gear_conf_cmd.enable)

# ---- special commands
gear.add_command(gear_special_cmd.term)
gear.add_command(gear_special_cmd.dtr0)
gear.add_command(gear_special_cmd.init)
gear.add_command(gear_special_cmd.rand)
gear.add_command(gear_special_cmd.comp)
gear.add_command(gear_special_cmd.withdraw)
gear.add_command(gear_special_cmd.ping)
gear.add_command(gear_special_cmd.search)
gear.add_command(gear_special_cmd.program)
gear.add_command(gear_special_cmd.verify)
gear.add_command(gear_special_cmd.dt)
gear.add_command(gear_special_cmd.dtr1)
gear.add_command(gear_special_cmd.dtr2)
gear.add_command(gear_special_cmd.write)
gear.add_command(gear_special_cmd.noreply)


@gear.group(name="query", help="Query gear status commands.")
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
gear_query.add_command(gear_special_cmd.short)

#
# ---- device commands
# @click.group(name="device", help="Control device commands.")
# def device():
#    pass
