import click
import dali

from .device_opcode import DeviceQueryCommandOpcode
from .device_action import query_device_value

device_addres_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be short address (0..63), group address (G0..G15), broadcast BC, or unaddressed BCU",
)

@click.command(name="status", help="Device status byte.")
@device_addres_option
def status(adr):
    result = query_device_value(adr, DeviceQueryCommandOpcode.STATUS)
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
