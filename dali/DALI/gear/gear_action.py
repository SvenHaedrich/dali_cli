"""Control gear action command implementation."""

import logging

import click
from dali_interface import DaliFrame, DaliInterface
from typeguard import typechecked

from ..system.constants import DaliFrameLength, DaliMax
from .gear_address import GearAddress
from .gear_opcode import GearSpecialCommandOpcode

logger = logging.getLogger(__name__)


@typechecked
def gear_send_forward_frame(dali: DaliInterface, adr_parameter: str, opcode: int, send_twice: bool = False):
    logger.debug("gear_send_forward_frame")
    address = GearAddress()
    if address.arg(adr_parameter):
        command = address.byte << 8 | opcode
        dali.transmit(DaliFrame(length=DaliFrameLength.GEAR, data=command, send_twice=send_twice))
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")


@typechecked
def query_gear_value(dali: DaliInterface, adr_parameter: str, opcode: int) -> int | None:
    logger.debug("gear_query_value")
    address = GearAddress()
    if address.arg(adr_parameter):
        command = address.byte << 8 | opcode
        reply = dali.query_reply(DaliFrame(length=DaliFrameLength.GEAR, data=command))
        if reply.length == DaliFrameLength.BACKWARD:
            return reply.data
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")
    return None


@typechecked
def query_gear_and_display_reply(dali: DaliInterface, adr_parameter: str, opcode: int) -> None:
    logger.debug("gear_query_and_display_reply")
    address = GearAddress()
    address.arg(adr_parameter)
    command = address.byte << 8 | opcode
    reply = dali.query_reply(DaliFrame(length=DaliFrameLength.GEAR, data=command))
    if reply.length == DaliFrameLength.BACKWARD:
        click.echo(f"0x{reply.data:02X} = {reply.data} = {reply.data:08b}b")
    else:
        click.echo(reply.message)


@typechecked
def set_gear_dtr0(dali: DaliInterface, value: int, parameter_hint: str = "UNKNOWN") -> None:
    logger.debug("set_dtr0")
    if 0 <= value < DaliMax.VALUE:
        command = GearSpecialCommandOpcode.DTR0 << 8 | value
        dali.transmit(DaliFrame(length=DaliFrameLength.GEAR, data=command), block=True)
    else:
        raise click.BadParameter(f"needs to be between 0 and {DaliMax.VALUE}.", param_hint=parameter_hint)


@typechecked
def set_gear_dtr1(dali: DaliInterface, value: int, parameter_hint: str = "UNKNOWN") -> None:
    logger.debug("set_dtr1")
    if 0 <= value < DaliMax.VALUE:
        command = GearSpecialCommandOpcode.DTR1 << 8 | value
        dali.transmit(DaliFrame(length=DaliFrameLength.GEAR, data=command), block=True)
    else:
        raise click.BadParameter(f"needs to be between 0 and {DaliMax.VALUE}.", param_hint=parameter_hint)


@typechecked
def write_gear_frame(
    dali: DaliInterface,
    address_byte: int,
    opcode_byte: int = 0,
    send_twice: bool = False,
) -> None:
    logger.debug("write_gear_frame")
    command = address_byte << 8 | opcode_byte
    dali.transmit(DaliFrame(length=DaliFrameLength.GEAR, data=command, send_twice=send_twice))


@typechecked
def write_gear_frame_and_wait(
    dali: DaliInterface,
    address_byte: int,
    opcode_byte: int = 0,
    send_twice: bool = False,
) -> None:
    logger.debug("write gear frame and wait for finish")
    frame = address_byte << 8 | opcode_byte
    dali.transmit(
        DaliFrame(length=DaliFrameLength.GEAR, data=frame, send_twice=send_twice),
        block=True,
    )


@typechecked
def write_frame_and_show_answer(dali: DaliInterface, address_byte: int, opcode_byte: int = 0):
    logger.debug("write_frame_and_show_answer")
    data = address_byte << 8 | opcode_byte
    reply = dali.query_reply(DaliFrame(length=DaliFrameLength.GEAR, data=data))
    if reply.length == DaliFrameLength.BACKWARD:
        click.echo(f"{reply.data} = 0x{reply.data:02X} = {reply.data:08b}b")
    else:
        click.echo(reply.message)
