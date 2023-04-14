from queue import Empty
from DALI.forward_frame_16bit import ForwardFrame16Bit
from DALI.address_byte import DALIAddressByte
from DALI.raw_frame import Raw_Frame

import click
import dali


def gear_query_multiple(adr, opcode):
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    dali.connection.write(cmd_frame)
    try:
        while True:
            frame = dali.connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                return frame.data
    except Empty:
        return None


def gear_summary_item(adr, caption, command_mnemonic):
    result = gear_query_multiple(adr, ForwardFrame16Bit.opcode(command_mnemonic))
    if not result == None:
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
    gear_summary_item(adr, "Status", "QUERY STATUS")
    gear_summary_item(adr, "Operation mode", "QUERY OPERATING MODE")
    gear_summary_item(adr, "Version", "QUERY VERSION NUMBER")
    gear_summary_item(adr, "Actual level", "QUERY ACTUAL LEVEL")
    gear_summary_item(adr, "Power on level", "QUERY POWER ON LEVEL")
    gear_summary_item(adr, "System failure level", "QUERY SYSTEM FAILURE LEVEL")
    gear_summary_item(adr, "Physical minimum", "QUERY PHYSICAL MINIMUM")
    gear_summary_item(adr, "Minimum level", "QUERY MIN LEVEL")
    gear_summary_item(adr, "Maximum level", "QUERY MAX LEVEL")
    gear_summary_item(adr, "Device type", "QUERY DEVICE TYPE")
    gear_summary_item(adr, "DTR0", "QUERY CONTENT DTR0")
    gear_summary_item(adr, "DTR1", "QUERY CONTENT DTR1")
    gear_summary_item(adr, "DTR2", "QUERY CONTENT DTR2")
    random_h = gear_query_multiple(
        adr, ForwardFrame16Bit.opcode("QUERY RANDOM ADDRESS (H)")
    )
    random_m = gear_query_multiple(
        adr, ForwardFrame16Bit.opcode("QUERY RANDOM ADDRESS (M)")
    )
    random_l = gear_query_multiple(
        adr, ForwardFrame16Bit.opcode("QUERY RANDOM ADDRESS (L)")
    )
    if not (random_h == None) and not (random_m == None) and not (random_l == None):
        random_address = random_h << 16 | random_m << 8 | random_l
        click.echo(
            f"Random address .....: {random_address} = 0x{random_address:06X} = {random_address:024b}b"
        )
    dali.connection.close()
