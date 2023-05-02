from queue import Empty
import click
import dali

from .opcode import QueryCommandOpcode
from .action import gear_send_forward_frame


@click.command(name="list", help="List available short addresses.")
def list():
    dali.connection.start_receive()
    address = "BC"
    cmd_frame = gear_send_forward_frame(address, QueryCommandOpcode.GEAR_PRESENT)
    answer = False
    try:
        while not answer:
            frame = dali.connection.read_raw_frame(dali.timeout_sec)
            if frame.data == cmd_frame.data:
                continue
            if frame:
                answer = True
    except Empty:
        pass
    if answer:
        click.echo("Found control gears:")
        for short_address in range(dali.MAX_ADR):
            address = f"{short_address:02}"
            cmd_frame = gear_send_forward_frame(
                address, QueryCommandOpcode.GEAR_PRESENT
            )
            answer = False
            try:
                while not answer:
                    frame = dali.connection.read_raw_frame(dali.timeout_sec)
                    if frame.data == cmd_frame.data:
                        continue
                    if frame.length == 8 and frame.data == 0xFF:
                        click.echo(f"G{short_address:02}")
            except Empty:
                pass
