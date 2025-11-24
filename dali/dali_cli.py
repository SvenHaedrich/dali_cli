"""Implement the main object of the DALI command line interface."""

import logging

import click

from .DALI.device import device_configure as device_configure_cmd
from .DALI.device import device_dump as device_dump_cmd
from .DALI.device import device_enumerate as device_enumerate_cmd
from .DALI.device import device_query as device_query_cmd
from .DALI.device import device_special as device_special_cmd
from .DALI.gear import gear_clear as gear_clear_cmd
from .DALI.gear import gear_configure as gear_conf_cmd
from .DALI.gear import gear_dump as gear_dump_cmd
from .DALI.gear import gear_enumerate as gear_enumerate_cmd
from .DALI.gear import gear_level as level_cmd
from .DALI.gear import gear_list as gear_list_cmd
from .DALI.gear import gear_query as gear_query_cmd
from .DALI.gear import gear_special as gear_special_cmd
from .DALI.gear import gear_summary as gear_summary_cmd
from .DALI.system.connection import dali_connection


@click.group(name="dali")
@click.version_option("0.2.5")
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
    "--on",
    help="Enable power supply (if available).",
    is_flag=True,
)
@click.option(
    "--off",
    help="Disable power supply (if available).",
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
def cli(ctx, serial_port, hid, mock, debug, on, off):  # pylint: disable=locally-disabled, too-many-arguments, too-many-positional-arguments
    """
    Command line interface for DALI systems.
    SevenLab 2025
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    dali_interface = "None"
    if serial_port and not hid and not mock:
        dali_interface = "Serial"

    if hid and not serial_port and not mock:
        dali_interface = "Usb"

    if mock and not serial_port and not hid:
        dali_interface = "Mock"
    ctx.obj = ctx.with_resource(dali_connection(dali_interface, serial_port))

    if hid and on:
        logging.debug("Enable power supply")
        ctx.obj.power(True)
    if hid and off:
        logging.debug("Disable power supply")
        ctx.obj.power(False)


cli.add_command(level_cmd.off)
cli.add_command(level_cmd.up)
cli.add_command(level_cmd.down)
cli.add_command(level_cmd.max_level)
cli.add_command(level_cmd.min_level)
cli.add_command(level_cmd.dapc)
cli.add_command(level_cmd.goto)


#
# ---- gear commands
@cli.group(name="gear", help="Control gear commands.")
def gear():
    pass


gear.add_command(gear_summary_cmd.summary)
gear.add_command(gear_list_cmd.gear_list)
gear.add_command(gear_dump_cmd.dump)
gear.add_command(gear_clear_cmd.clear)

# ---- configure commands
gear.add_command(gear_conf_cmd.reset)
gear.add_command(gear_conf_cmd.actual)
gear.add_command(gear_conf_cmd.op)
gear.add_command(gear_conf_cmd.reset_mem)
gear.add_command(gear_conf_cmd.identify)
gear.add_command(gear_conf_cmd.max_level)
gear.add_command(gear_conf_cmd.min_level)
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
gear.add_command(gear_enumerate_cmd.gear_enumerate)


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


# ---- query commands
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
gear_query.add_command(gear_query_cmd.fade)
gear_query.add_command(gear_special_cmd.short)


#
# ---- device commands
@cli.group(name="device", help="Control device commands.")
def device():
    pass


device.add_command(device_dump_cmd.dump)
device.add_command(device_special_cmd.dtr0)
device.add_command(device_special_cmd.dtr1)
device.add_command(device_special_cmd.dtr2)
device.add_command(device_special_cmd.init)
device.add_command(device_special_cmd.rand)
device.add_command(device_special_cmd.testframe)

#
# ---- configure commands
device.add_command(device_configure_cmd.add)
device.add_command(device_configure_cmd.start)
device.add_command(device_configure_cmd.stop)
device.add_command(device_configure_cmd.reset)
device.add_command(device_configure_cmd.ungroup)
device.add_command(device_configure_cmd.short)
device.add_command(device_configure_cmd.scheme)
device.add_command(device_configure_cmd.primary)
device.add_command(device_configure_cmd.application)
device.add_command(device_configure_cmd.cycle)
device.add_command(device_enumerate_cmd.device_enumerate)


@device.group(name="query", help="Query device status commands")
def device_query():
    pass


# ---- query commands
device_query.add_command(device_query_cmd.capabilities)
device_query.add_command(device_query_cmd.dtr0)
device_query.add_command(device_query_cmd.dtr1)
device_query.add_command(device_query_cmd.dtr2)
device_query.add_command(device_query_cmd.extended)
device_query.add_command(device_query_cmd.groups)
device_query.add_command(device_query_cmd.quiescent)
device_query.add_command(device_query_cmd.status)
device_query.add_command(device_query_cmd.short)
device_query.add_command(device_query_cmd.version)
device_query.add_command(device_query_cmd.random)
device_query.add_command(device_query_cmd.reset)
device_query.add_command(device_query_cmd.scheme)
device_query.add_command(device_query_cmd.itype)
device_query.add_command(device_query_cmd.resolution)
device_query.add_command(device_query_cmd.error)
device_query.add_command(device_query_cmd.istatus)
device_query.add_command(device_query_cmd.enabled)
device_query.add_command(device_query_cmd.primary)
