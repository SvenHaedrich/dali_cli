"""Control device actions implementations"""

import logging

import click
from typeguard import typechecked

from ..dali_interface.dali_interface import DaliFrame, DaliInterface
from ..system.constants import DaliFrameLength, DaliMax
from .device_address import DaliDeviceAddressByte
from .device_opcode import DeviceSpecialCommandOpcode

logger = logging.getLogger(__name__)


@typechecked
def query_device_value(
    dali: DaliInterface, adr_parameter: str, opcode: int
) -> int | None:
    logger.debug("query_device_value")
    address = DaliDeviceAddressByte()
    instance = 0xFE
    if address.arg(adr_parameter):
        command = (address.byte << 16) | (instance << 8) | opcode
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
        command = 0xC1 << 16 | DeviceSpecialCommandOpcode.DTR0 << 8 | value
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
        command = 0xC1 << 16 | DeviceSpecialCommandOpcode.DTR1 << 8 | value
        dali.transmit(
            DaliFrame(length=DaliFrameLength.DEVICE, data=command), block=True
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE}.", param_hint=parameter_hint
        )
