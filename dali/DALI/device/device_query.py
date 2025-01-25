"""Control device query commands implementation."""

import click

from ..dali_interface.dali_interface import DaliInterface
from .device_action import query_device_value
from .device_opcode import DeviceQueryCommandOpcode

device_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be short address (0..63), group address (G0..G15), broadcast BC, or unaddressed BCU",
)


@click.command(
    name="status",
    help="Query control device status byte. The answer shall be the status, which is formed by a combination of control device properties.",
)
@click.pass_obj
@device_address_option
def status(dali: DaliInterface, adr):
    result = query_device_value(dali, adr, DeviceQueryCommandOpcode.QUERY_STATUS)
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


@click.command(name="version", help="Query control device version number.")
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


@click.command(
    name="capabilities",
    help="Query control device capabilities. The answer shall be a combination of control device capabilities.",
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


@click.command(name="dtr0", help="Query content of DTR0.")
@click.pass_obj
@device_address_option
def dtr0(dali: DaliInterface, adr):
    result = query_device_value(dali, adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR0)
    if result is not None:
        click.echo(f"DTR0: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="dtr1", help="Query content of DTR1.")
@click.pass_obj
@device_address_option
def dtr1(dali: DaliInterface, adr):
    result = query_device_value(dali, adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR1)
    if result is not None:
        click.echo(f"DTR1: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="dtr2", help="Query content of DTR2.")
@click.pass_obj
@device_address_option
def dtr2(dali: DaliInterface, adr):
    result = query_device_value(dali, adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR2)
    if result is not None:
        click.echo(f"DTR2: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="quiescent", help="Query content of DTR2.")
@click.pass_obj
@device_address_option
def quiescent(dali: DaliInterface, adr):
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_QUIESCENT_MODE
    )
    if result is not None:
        click.echo(f"{result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")


@click.command(name="groups", help="Query device group settings.")
@click.pass_obj
@device_address_option
def groups(dali: DaliInterface, adr):
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_GROUPS_0_7
    )
    if result is None:
        click.echo("timeout - NO")
        return
    click.echo(f"GROUPS  0- 7: {result} = 0x{result:02X} = {result:08b}b")
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_GROUPS_8_15
    )
    if result is None:
        click.echo("timeout - NO")
        return
    click.echo(f"GROUPS  8-15: {result} = 0x{result:02X} = {result:08b}b")
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_GROUPS_16_23
    )
    if result is None:
        click.echo("timeout - NO")
        return
    click.echo(f"GROUPS 16-23: {result} = 0x{result:02X} = {result:08b}b")
    result = query_device_value(
        dali, adr, DeviceQueryCommandOpcode.QUERY_DEVICE_GROUPS_24_31
    )
    if result is None:
        click.echo("timeout - NO")
        return
    click.echo(f"GROUPS 24-31: {result} = 0x{result:02X} = {result:08b}b")
