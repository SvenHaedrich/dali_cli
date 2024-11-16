"""Control gear action command implementation."""

import logging

import click
from typeguard import typechecked

from ..dali_interface.dali_interface import DaliFrame
from ..system.constants import DaliMax
from .address import DaliAddressByte
from .gear_opcode import GearSpecialCommandOpcode

logger = logging.getLogger(__name__)


@typechecked
def gear_send_forward_frame(
    adr_parameter: str, opcode: int, send_twice: bool = False, close: bool = True
):
    logger.debug("gear_send_forward_frame")
    address = DaliAddressByte()
    if address.arg(adr_parameter):
        command = address.byte << 8 | opcode
        dali.connection.transmit(
            DaliFrame(length=16, data=command, send_twice=send_twice)
        )
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")
    if close:
        dali.connection.close()


@typechecked
def query_gear_value(adr_parameter: str, opcode: int, close: bool = True) -> int | None:
    logger.debug("gear_query_value")
    address = DaliAddressByte()
    if address.arg(adr_parameter):
        command = address.byte << 8 | opcode
        reply = dali.connection.query_reply(DaliFrame(length=16, data=command))
        if reply.length == 8:
            return reply.data
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")
    if close:
        dali.connection.close()
    return None


@typechecked
def query_gear_and_display_reply(
    adr_parameter: str, opcode: int, close: bool = True
) -> None:
    logger.debug("gear_query_and_display_reply")
    address = DaliAddressByte()
    address.arg(adr_parameter)
    command = address.byte << 8 | opcode
    reply = dali.connection.query_reply(DaliFrame(length=16, data=command))
    if reply.length == 8:
        click.echo(f"0x{reply.data:02X} = " f"{reply.data} = " f"{reply.data:08b}b")
    else:
        click.echo(reply.message)
    if close:
        dali.connection.close()


@typechecked
def set_dtr0(value: int, parameter_hint: str = "UNKNOWN") -> None:
    logger.debug("set_dtr0")
    if 0 <= value < DaliMax.VALUE:
        command = GearSpecialCommandOpcode.DTR0 << 8 | value
        dali.connection.transmit(DaliFrame(length=16, data=command), block=True)
    else:
        raise click.BadParameter(
            "needs to be between 0 and 255.", param_hint=parameter_hint
        )


@typechecked
def set_dtr1(value: int, parameter_hint: str = "UNKNOWN") -> None:
    logger.debug("set_dtr1")
    if 0 <= value < DaliMax.VALUE:
        command = GearSpecialCommandOpcode.DTR1 << 8 | value
        dali.connection.transmit(DaliFrame(length=16, data=command), block=True)
    else:
        raise click.BadParameter(
            "needs to be between 0 and 255.", param_hint=parameter_hint
        )


@typechecked
def write_gear_frame(
    address_byte: int, opcode_byte: int = 0, send_twice: bool = False
) -> None:
    logger.debug("write_gear_frame")
    command = address_byte << 8 | opcode_byte
    dali.connection.transmit(DaliFrame(length=16, data=command, send_twice=send_twice))


@typechecked
def write_frame_and_show_answer(address_byte: int, opcode_byte: int = 0):
    logger.debug("write_frame_and_show_answer")
    data = address_byte << 8 | opcode_byte
    reply = dali.connection.query_reply(DaliFrame(length=16, data=data))
    if reply.length == 8:
        click.echo(f"{reply.data} = " f"0x{reply.data:02X} = " f"{reply.data:08b}b")
    else:
        click.echo(reply.message)
