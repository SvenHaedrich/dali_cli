from queue import Empty
import click
import dali

from .opcode import QueryCommandOpcode
from .action import gear_send_forward_frame


@click.command(name="list", help="List available short addresses.")
def list():
    dali.connection.start_receive()
    address = "BC"
    gear_send_forward_frame(address, QueryCommandOpcode.GEAR_PRESENT)
    answer = False
    try:
        while not answer:
            dali.connection.get_next(dali.timeout_sec)
            if dali.connection.data == dali.connection.last_transmit:
                continue
            answer = True
    except Empty:
        pass
    if answer:
        click.echo("Found control gears:")
        for short_address in range(dali.MAX_ADR):
            address = f"{short_address:02}"
            gear_send_forward_frame(address, QueryCommandOpcode.GEAR_PRESENT)
            answer = False
            try:
                while not answer:
                    click.echo(message=f"{short_address}\r", nl=False)
                    dali.connection.get_next(dali.timeout_sec)
                    if dali.connection.data == dali.connection.last_transmit:
                        continue
                    if dali.connection.length == 8 and dali.connection.data == 0xFF:
                        click.echo(f"G{short_address:02}")
            except Empty:
                pass
    dali.connection.close()
