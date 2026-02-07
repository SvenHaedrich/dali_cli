"""Control device actions implementations"""

import logging

import click
from dali_interface import DaliFrame, DaliInterface

from ..system.constants import DaliFrameLength
from .device_address import DeviceAddress, InstanceAddress
from .device_opcode import DeviceSpecialCommandOpcode

logger = logging.getLogger(__name__)


def query_instance_value(dali: DaliInterface, adr_parameter: str, instance_parameter: str, opcode: int) -> int | None:
    """Query a value from a control device instance"""
    address = DeviceAddress(adr_parameter)
    instance = InstanceAddress(instance_parameter)
    if not instance.isvalid():
        raise click.BadOptionUsage("instance", "invalid instance option.")
    if not address.isvalid():
        raise click.BadOptionUsage("adr", "invalid address option.")
    command = (address.byte << 16) | (instance.byte << 8) | opcode
    reply = dali.query_reply(DaliFrame(length=DaliFrameLength.DEVICE, data=command))
    if reply.length == DaliFrameLength.BACKWARD:
        return reply.data
    return None


def query_device_value(dali: DaliInterface, adr_parameter: str, opcode: int) -> int | None:
    """Query a value from a control device"""
    return query_instance_value(dali, adr_parameter, "DEVICE", opcode)


def set_device_dtr0(dali: DaliInterface, value: int) -> None:
    """Set control device data transfer register 0"""
    logger.debug("set_device_dtr0")
    address = DeviceAddress("SPECIAL")
    command = address.byte << 16 | DeviceSpecialCommandOpcode.DTR0 << 8 | value
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=command), block=True)


def set_device_dtr1(dali: DaliInterface, value: int) -> None:
    """Set control device data transfer register 1"""
    logger.debug("set_device_dtr1")
    address = DeviceAddress("SPECIAL")
    command = address.byte << 16 | DeviceSpecialCommandOpcode.DTR1 << 8 | value
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=command), block=True)


def write_device_frame(
    dali: DaliInterface,
    address_byte: int = 0,
    instance_byte: int = 0,
    opcode_byte: int = 0,
    send_twice: bool = False,
) -> None:
    """Assemble a control device frame and transmit it"""
    logger.debug("write_device_frame")
    frame = address_byte << 16 | instance_byte << 8 | opcode_byte
    dali.transmit(
        DaliFrame(length=DaliFrameLength.DEVICE, data=frame, send_twice=send_twice),
        block=True,
    )


def set_device_dtr2_dtr1(dali: DaliInterface, dtr2: int, dtr1: int) -> None:
    """Set control device data transfer registers 0 and 1 simultaneously"""
    write_device_frame(dali, DeviceSpecialCommandOpcode.DTR2_DTR1, dtr2, dtr1)
