from queue import Empty
import click
import dali

from .action import gear_send_forward_frame
from .opcode import QueryCommandOpcode


def gear_query_multiple(adr, opcode):
    cmd_frame = gear_send_forward_frame(adr, opcode)
    try:
        while True:
            frame = dali.connection.read_raw_frame(dali.timeout_sec)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                return frame.data
    except Empty:
        return None


def gear_summary_item(adr, caption, opcode):
    result = gear_query_multiple(adr, opcode)
    if result is not None:
        click.echo(f"{caption:.<20}: {result} = 0x{result:02X} = {result:08b}b")
    else:
        click.echo(f"{caption:.<20}: NO - timeout")


@click.command(name="summary", help="Show status summary.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def summary(adr):
    dali.connection.start_read()
    gear_summary_item(adr, "Status", QueryCommandOpcode.STATUS)
    gear_summary_item(adr, "Operation mode", QueryCommandOpcode.OPERATING_MODE)
    gear_summary_item(adr, "Version", QueryCommandOpcode.VERSION_NUMBER)
    gear_summary_item(adr, "Actual level", QueryCommandOpcode.ACTUAL_LEVEL)
    gear_summary_item(adr, "Power on level", QueryCommandOpcode.POWER_ON_LEVEL)
    gear_summary_item(
        adr, "System failure level", QueryCommandOpcode.SYSTEM_FAILURE_LEVEL
    )
    gear_summary_item(adr, "Physical minimum", QueryCommandOpcode.PHYSICAL_MINIMUM)
    gear_summary_item(adr, "Minimum level", QueryCommandOpcode.MIN_LEVEL)
    gear_summary_item(adr, "Maximum level", QueryCommandOpcode.MAX_LEVEL)
    gear_summary_item(adr, "Device type", QueryCommandOpcode.DEVICE_TYPE)
    gear_summary_item(adr, "DTR0", QueryCommandOpcode.CONTENT_DTR0)
    gear_summary_item(adr, "DTR1", QueryCommandOpcode.CONTENT_DTR1)
    gear_summary_item(adr, "DTR2", QueryCommandOpcode.CONTENT_DTR2)
    random_h = gear_query_multiple(adr, QueryCommandOpcode.RANDOM_ADDRESS_H)
    random_m = gear_query_multiple(adr, QueryCommandOpcode.RANDOM_ADDRESS_M)
    random_l = gear_query_multiple(adr, QueryCommandOpcode.RANDOM_ADDRESS_L)
    if (random_h is not None) and (random_m is not None) and (random_l is not None):
        random_address = random_h << 16 | random_m << 8 | random_l
        click.echo(
            f"Random address .....: {random_address} = 0x{random_address:06X} = {random_address:024b}b"
        )
