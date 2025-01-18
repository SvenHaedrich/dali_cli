"""Control device special commands implementation."""

import click

from ..dali_interface.dali_interface import DaliInterface
from ..system.constants import DaliMax
from .device_action import write_device_frame
from .device_opcode import DeviceSpecialCommandOpcode


@click.command(name="dtr0", help="Set data transfer register 0")
@click.pass_obj
@click.argument("data", type=click.INT)
def dtr0(dali: DaliInterface, data):
    if 0 <= data < DaliMax.VALUE:
        write_device_frame(
            dali,
            DeviceSpecialCommandOpcode.SPECIAL_CMD,
            DeviceSpecialCommandOpcode.DTR0,
            data,
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE-1}.", param_hint="DATA"
        )


@click.command(name="dtr1", help="Set data transfer register 1")
@click.pass_obj
@click.argument("data", type=click.INT)
def dtr1(dali: DaliInterface, data):
    if 0 <= data < DaliMax.VALUE:
        write_device_frame(
            dali,
            DeviceSpecialCommandOpcode.SPECIAL_CMD,
            DeviceSpecialCommandOpcode.DTR1,
            data,
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE-1}.", param_hint="DATA"
        )


@click.command(name="dtr2", help="Set data transfer register 2")
@click.pass_obj
@click.argument("data", type=click.INT)
def dtr2(dali: DaliInterface, data):
    if 0 <= data < DaliMax.VALUE:
        write_device_frame(
            dali,
            DeviceSpecialCommandOpcode.SPECIAL_CMD,
            DeviceSpecialCommandOpcode.DTR2,
            data,
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE-1}.", param_hint="DATA"
        )


@click.command(name="testframe", help="Send a test frame")
@click.pass_obj
@click.argument("priority", type=click.INT, default=5)
@click.argument("repeat", type=click.INT, default=0)
@click.argument("gear", type=click.BOOL, default=False)
def testframe(dali: DaliInterface, priority, repeat, gear):
    if not 0 < priority <= DaliMax.PRIORITY:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.PRIORITY}.", param_hint="PRIORITY"
        )
    if not 0 <= repeat <= 3:
        raise click.BadParameter("needs to be between 0 and 3.", param_hint="REPEAT")
    data = priority | repeat << 3
    if gear:
        data = data | 0x20
    write_device_frame(
        dali,
        DeviceSpecialCommandOpcode.SPECIAL_CMD,
        DeviceSpecialCommandOpcode.SEND_TESTFRAME,
        data,
    )
