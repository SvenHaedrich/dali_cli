import click
import dali
import logging
from typeguard import typechecked


from .device_address import DaliDeviceAddressByte
from .device_opcode import DeviceSpecialCommandOpcode

from ..dali_interface.dali_interface import DaliFrame


logger = logging.getLogger(__name__)


@typechecked
def query_device_value(
    adr_parameter: str, opcode: int, close: bool = True
) -> int | None:
    logger.debug("gear_device_value")
    address = DaliDeviceAddressByte()
    instance = 0xFE
    if address.arg(adr_parameter):
        command = (address.byte << 16) | (instance << 8) | opcode
        reply = dali.connection.query_reply(DaliFrame(length=24, data=command))
        if reply.length == 8:
            return reply.data
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")
    if close:
        dali.connection.close()
    return None


@typechecked
def set_device_dtr0(value: int, parameter_hint: str = "UNKNOWN") -> None:
    logger.debug("set_device_dtr0")
    if 0 <= value < dali.MAX_VALUE:
        command = 0xC1 << 16 | DeviceSpecialCommandOpcode.DTR0 << 8 | value
        dali.connection.transmit(DaliFrame(length=24, data=command), block=True)
    else:
        raise click.BadParameter(
            "needs to be between 0 and 255.", param_hint=parameter_hint
        )


@typechecked
def set_device_dtr1(value: int, parameter_hint: str = "UNKNOWN") -> None:
    logger.debug("set_device_dtr1")
    if 0 <= value < dali.MAX_VALUE:
        command = 0xC1 << 16 | DeviceSpecialCommandOpcode.DTR1 << 8 | value
        dali.connection.transmit(DaliFrame(length=24, data=command), block=True)
    else:
        raise click.BadParameter(
            "needs to be between 0 and 255.", param_hint=parameter_hint
        )
