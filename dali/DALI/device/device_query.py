import click
import dali

from .device_opcode import DeviceQueryCommandOpcode
from .device_action import query_device_value

device_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be short address (0..63), group address (G0..G15), broadcast BC, or unaddressed BCU",
)


@click.command(name="status", help="Device status byte.")
@device_address_option
def status(adr):
    result = query_device_value(adr, DeviceQueryCommandOpcode.QUERY_STATUS)
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
    dali.connection.close()


@click.command(name="version", help="Device version number")
@device_address_option
def version(adr):
    result = query_device_value(adr, DeviceQueryCommandOpcode.QUERY_VERSION_NUMBER)
    if result is not None:
        major_version = result >> 2
        minor_version = result & 7
        click.echo(
            f"version: {result} = 0x{result:02X} = {result:08b}b = {major_version}.{minor_version}"
        )
    else:
        click.echo("timeout - NO")
    dali.connection.close()


@click.command(name="capabilities", help="Device capabilities")
@device_address_option
def capabilities(adr):
    result = query_device_value(adr, DeviceQueryCommandOpcode.QUERY_DEVICE_CAPABILITIES)
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
    dali.connection.close()


@click.command(name="dtr0", help="Device content of DTR0")
@device_address_option
def dtr0(adr):
    result = query_device_value(adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR0)
    if result is not None:
        click.echo(f"DTR0: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")
    dali.connection.close()


@click.command(name="dtr1", help="Device content of DTR1")
@device_address_option
def dtr1(adr):
    result = query_device_value(adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR1)
    if result is not None:
        click.echo(f"DTR1: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")
    dali.connection.close()


@click.command(name="dtr2", help="Device content of DTR2")
@device_address_option
def dtr2(adr):
    result = query_device_value(adr, DeviceQueryCommandOpcode.QUERY_CONTENT_DTR2)
    if result is not None:
        click.echo(f"DTR2: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo("timeout - NO")
    dali.connection.close()
