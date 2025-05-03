"""Control device query commands implementation."""

import click

from ..dali_interface.dali_interface import DaliFrame, DaliInterface
from ..system.constants import DaliFrameLength, DaliMax
from .device_action import query_device_value, query_instance_value, set_device_dtr0
from .device_address import DeviceAddress, InstanceAddress
from .device_opcode import (
    DeviceInstanceQueryOpcode,
    DeviceQueryCommandOpcode,
    DeviceSpecialCommandOpcode,
)

device_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be short address (0..63), group address (G0..G15), broadcast BC, or unaddressed BCU",
)

instance_address_option = click.option(
    "--instance",
    default="BC",
    help="Instance address, can be instance number (0..31), group (G0..G31), type (T0..T31), or broadcast BC",
)


@click.command(
    name="status",
    help="Control device status byte. The answer shall be the status, which is formed by a combination of control device properties.",
)
@click.pass_obj
@device_address_option
def status(dali: DaliInterface, adr):
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_STATUS
    )
    if result is not None:
        click.echo(f"status: {result} = 0x{result:02X} = {result:08b}b")
        click.echo("bit : description")
        click.echo(f"  {(result >> 0 & 0x01)} : inputDeviceError")
        click.echo(f"  {(result >> 1 & 0x01)} : quiescentMode")
        click.echo(f"  {(result >> 2 & 0x01)} : shortAddress is Mask")
        click.echo(f"  {(result >> 3 & 0x01)} : applicationActive")
        click.echo(f"  {(result >> 4 & 0x01)} : applicationControllerError")
        click.echo(f"  {(result >> 5 & 0x01)} : powerCycleSeen")
        click.echo(f"  {(result >> 6 & 0x01)} : resetState")
        click.echo(f"  {(result >> 7 & 0x01)} : unused")
    else:
        click.echo("timeout - NO")


@click.command(name="version", help="Control device version number.")
@click.pass_obj
@device_address_option
def version(dali: DaliInterface, adr):
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_VERSION_NUMBER
    )
    if result is not None:
        major_version = result >> 2
        minor_version = result & 7
        click.echo(
            f"version: {result} = 0x{result:02X} = {result:08b}b = {major_version}.{minor_version}"
        )
    else:
        click.echo("timeout - NO")


@click.command(name="extended", help="Control device extended version number for 30X.")
@click.pass_obj
@click.argument("x", type=click.INT)
@device_address_option
def extended(dali: DaliInterface, x, adr):
    if 0 <= x <= DaliMax.VALUE:
        set_device_dtr0(dali, x)
        result = query_device_value(
            dali, adr, DeviceQueryCommandOpcode.QUERY_EXTENDED_VERSION_NUMBER
        )
        if result is not None:
            major_version = result >> 2
            minor_version = result & 7
            click.echo(
                f"version: {result} = 0x{result:02X} = {result:08b}b = {major_version}.{minor_version}"
            )
        else:
            click.echo("timeout - NO")
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE-1}.", param_hint="X"
        )


@click.command(
    name="capabilities",
    help="Control device capabilities. The answer shall be a combination of control device capabilities.",
)
@click.pass_obj
@device_address_option
def capabilities(dali: DaliInterface, adr):
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_CAPABILITIES
    )
    if result is not None:
        click.echo(f"status: {result} = 0x{result:02X} = {result:08b}b")
        click.echo("bit : description")
        click.echo(f"  {(result >> 0 & 0x01)} : applicationControllerPresent")
        click.echo(f"  {(result >> 1 & 0x01)} : numberOfInstances > 0")
        click.echo(f"  {(result >> 2 & 0x01)} : applicationControllerAlwaysActive")
        click.echo(f"  {(result >> 3 & 0x01)} : reserved for IEC 62386-104")
        click.echo(f"  {(result >> 4 & 0x01)} : reserved for IEC 62386-104")
        click.echo(
            f"  {(result >> 5 & 0x01)} : At least one instance supports instanceType configuration"
        )
        click.echo(f"  {(result >> 6 & 0x01)} : unused")
        click.echo(f"  {(result >> 7 & 0x01)} : unused")
    else:
        click.echo("timeout - NO")


@click.command(name="reset", help="Reset state of all variables.")
@click.pass_obj
@device_address_option
def reset(dali: DaliInterface, adr):
    result = query_device_value(dali, adr, DeviceQueryCommandOpcode.QUERY_RESET_STATE)
    if result is None:
        click.echo("timeout - NO")
    elif result == DaliMax.MASK:
        click.echo("YES")
    else:
        click.echo(f"{result} = 0x{result:02X} = {result:08b}b")


@click.command(name="dtr0", help="Content of DTR0.")
@click.pass_obj
@device_address_option
def dtr0(dali: DaliInterface, adr):
    result = query_device_value(dali, adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR0)
    if result is not None:
        click.echo(f"DTR0: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="dtr1", help="Content of DTR1.")
@click.pass_obj
@device_address_option
def dtr1(dali: DaliInterface, adr):
    result = query_device_value(dali, adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR1)
    if result is not None:
        click.echo(f"DTR1: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="dtr2", help="Content of DTR2.")
@click.pass_obj
@device_address_option
def dtr2(dali: DaliInterface, adr):
    result = query_device_value(dali, adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR2)
    if result is not None:
        click.echo(f"DTR2: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="short", help="shortAddress.")
@click.pass_obj
def short(dali: DaliInterface):
    address = DeviceAddress("SPECIAL")
    data = (address.byte << 16) | (DeviceSpecialCommandOpcode.QUERY_SHORT_ADDRESS << 8)
    reply = dali.query_reply(DaliFrame(length=DaliFrameLength.DEVICE, data=data))
    if reply.length == DaliFrameLength.BACKWARD:
        click.echo(
            f"short address: {reply.data} = 0x{reply.data:02X} = {reply.data:08b}b"
        )
    else:
        click.echo("timeout - NO")


@click.command(name="random", help="randomAddress.")
@click.pass_obj
@device_address_option
def random(dali: DaliInterface, adr):
    random_h = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_RANDOM_ADDRESS_H
    )
    random_m = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_RANDOM_ADDRESS_M
    )
    random_l = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_RANDOM_ADDRESS_L
    )
    if (random_h is None) or (random_m is None) or (random_l is None):
        click.echo("timeout - NO")
    else:
        random_address = random_h << 16 | random_m << 8 | random_l
        click.echo(
            f"random address: 0x{random_address:06X} = "
            f"{random_address:024b}b = "
            f"{random_address}"
        )


@click.command(name="quiescent", help="Content of DTR2.")
@click.pass_obj
@device_address_option
def quiescent(dali: DaliInterface, adr):
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_QUIESCENT_MODE
    )
    if result is not None:
        click.echo(f"quiescent: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="groups", help="Device group settings.")
@click.pass_obj
@device_address_option
def groups(dali: DaliInterface, adr):
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_GROUPS_0_7
    )
    if result is None:
        click.echo("timeout - NO")
        return
    click.echo(f"groups  0- 7: {result:3} = 0x{result:02X} = {result:08b}b")
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_GROUPS_8_15
    )
    if result is None:
        click.echo("timeout - NO")
        return
    click.echo(f"groups  8-15: {result:3} = 0x{result:02X} = {result:08b}b")
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_GROUPS_16_23
    )
    if result is None:
        click.echo("timeout - NO")
        return
    click.echo(f"groups 16-23: {result:3} = 0x{result:02X} = {result:08b}b")
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_GROUPS_24_31
    )
    if result is None:
        click.echo("timeout - NO")
        return
    click.echo(f"groups 24-31: {result:3} = 0x{result:02X} = {result:08b}b")


@click.command(name="scheme", help="Event scheme setting.")
@click.pass_obj
@device_address_option
@instance_address_option
def scheme(dali: DaliInterface, adr: str, instance: str):
    address = DeviceAddress(adr)
    instance = InstanceAddress(instance)
    if address.isvalid() and instance.isvalid():
        result = query_device_value(
            dali, adr, DeviceInstanceQueryOpcode.QUERY_EVENT_SCHEME
        )
        if result is not None:
            click.echo(f"event scheme {result} = 0x{result:02X} = {result:08b}b")
            if result == 0:
                click.echo("Instance addressing, using instance type and number.")
            elif result == 1:
                click.echo("Device addressing, using short address and instance type.")
            elif result == 2:
                click.echo(
                    "Device and instance addressing, using short address and instance number."
                )
            elif result == 3:
                click.echo(
                    "Device group addressing, using device group and instance type."
                )
            elif result == 4:
                click.echo("Instance group addressing, using instance group and type.")
            else:
                click.echo("Invalid event scheme.")
        else:
            click.echo("timeout - NO")


@click.command(name="type", help="Instance type.")
@click.pass_obj
@device_address_option
@instance_address_option
def itype(dali: DaliInterface, adr: str, instance: str):
    """11.9.2 QUERY INSTANCE TYPE"""
    result = query_instance_value(
        dali, adr, instance, DeviceInstanceQueryOpcode.QUERY_INSTANCE_TYPE
    )
    if result is not None:
        click.echo(f"type {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="resolution", help="Instance resolution.")
@click.pass_obj
@device_address_option
@instance_address_option
def resolution(dali: DaliInterface, adr: str, instance: str):
    """11.9.3 QUERY RESOLUTION"""
    result = query_instance_value(
        dali, adr, instance, DeviceInstanceQueryOpcode.QUERY_RESOLUTION
    )
    if result is not None:
        click.echo(f"resolution {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="error", help="Instance error information.")
@click.pass_obj
@device_address_option
@instance_address_option
def error(dali: DaliInterface, adr: str, instance: str):
    """11.9.4 QUERY INSTANCE ERROR"""
    result = query_instance_value(
        dali, adr, instance, DeviceInstanceQueryOpcode.QUERY_INSTANCE_ERROR
    )
    if result is not None:
        click.echo(f"error {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="istatus", help="Instance status information.")
@click.pass_obj
@device_address_option
@instance_address_option
def istatus(dali: DaliInterface, adr: str, instance: str):
    """11.9.5 QUERY INSTANCE STATUS"""
    result = query_instance_value(
        dali, adr, instance, DeviceInstanceQueryOpcode.QUERY_INSTANCE_STATUS
    )
    if result is not None:
        click.echo(f"status: {result} = 0x{result:02X} = {result:08b}b")
        click.echo("bit : description")
        click.echo(f"  {(result >> 0 & 0x01)} : instanceError")
        click.echo(f"  {(result >> 1 & 0x01)} : instanceActive")
    else:
        click.echo("timeout - NO")


@click.command(name="enabled", help="Instance active information.")
@click.pass_obj
@device_address_option
@instance_address_option
def enabled(dali: DaliInterface, adr: str, instance: str):
    """11.9.6 QUERY INSTANCE ENABLED"""
    result = query_instance_value(
        dali, adr, instance, DeviceInstanceQueryOpcode.QUERY_INSTANCE_ENABLED
    )
    if result is None:
        click.echo("timeout - NO")
    elif result == DaliMax.MASK:
        click.echo("YES")
    else:
        click.echo(f"{result} = 0x{result:02X} = {result:08b}b")


@click.command(name="primary", help="Primary instance group setting.")
@click.pass_obj
@device_address_option
@instance_address_option
def primary(dali: DaliInterface, adr: str, instance: str):
    """11.9.7 QUERY PRIMARY INSTANCE GROUP"""
    result = query_instance_value(
        dali, adr, instance, DeviceInstanceQueryOpcode.QUERY_PRIMARY_INSTANCE_GROUP
    )
    if result is not None:
        click.echo(f"primary group {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")
