"""Control device actions implementations"""

import logging

import click
from typeguard import typechecked

from ..dali_interface.dali_interface import DaliFrame, DaliInterface
from ..system.constants import DaliFrameLength, DaliMax
from .device_address import DeviceAddress, InstanceAddress
from .device_opcode import DeviceSpecialCommandOpcode

logger = logging.getLogger(__name__)


@typechecked
def query_device_value(
    dali: DaliInterface, adr_parameter: str, opcode: int
) -> int | None:
    logger.debug("query_device_value")
    address = DeviceAddress(adr_parameter)
    instance = InstanceAddress()
    instance.device()
    if address.isvalid():
        command = (address.byte << 16) | (instance.byte << 8) | opcode
        reply = dali.query_reply(DaliFrame(length=DaliFrameLength.DEVICE, data=command))
        if reply.length == DaliFrameLength.BACKWARD:
            return reply.data
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")
    return None


@typechecked
def set_device_dtr0(
    dali: DaliInterface, value: int, parameter_hint: str = "UNKNOWN"
) -> None:
    logger.debug("set_device_dtr0")
    if 0 <= value < DaliMax.VALUE:
        address = DeviceAddress()
        address.special()
        command = (
            address.byte << 16
            | DeviceSpecialCommandOpcode.DTR0 << 8
            | value
        )
        dali.transmit(
            DaliFrame(length=DaliFrameLength.DEVICE, data=command), block=True
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE}.", param_hint=parameter_hint
        )


@typechecked
def set_device_dtr1(
    dali: DaliInterface, value: int, parameter_hint: str = "UNKNOWN"
) -> None:
    logger.debug("set_device_dtr1")
    if 0 <= value < DaliMax.VALUE:
        address = DeviceAddress()
        address.special()
        command = (
            address.byte << 16
            | DeviceSpecialCommandOpcode.DTR1 << 8
            | value
        )
        dali.transmit(
            DaliFrame(length=DaliFrameLength.DEVICE, data=command), block=True
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE}.", param_hint=parameter_hint
        )


@typechecked
def write_device_frame(
    dali: DaliInterface,
    address_byte: int = 0,
    instance_byte: int = 0,
    opcode_byte: int = 0,
    send_twice: bool = False,
) -> None:
    logger.debug("write_device_frame")
    frame = address_byte << 16 | instance_byte << 8 | opcode_byte
    dali.transmit(
        DaliFrame(length=DaliFrameLength.DEVICE, data=frame, send_twice=send_twice),
        block=True,
    )


@typechecked
def set_device_dtr2_dtr1(dali: DaliInterface, dtr2: int, dtr1: int) -> None:
    write_device_frame(dali, DeviceSpecialCommandOpcode.DTR2_DTR1, dtr2, dtr1)
