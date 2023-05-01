from queue import Empty
import click

from DALI.gear import action
from DALI.gear import opcode


@click.command(name="list", help="List available short addresses.")
def list():
    dali.connection.start_read()
    opcode = QueryCommandOpcode.GEAR_PRESENT
    address = DALIAddressByte()
    address.broadcast()
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    dali.connection.write(cmd_frame)
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
        for short_address in range(0x40):
            address.short(short_address)
            command = address.byte << 8 | opcode
            frame = Raw_Frame(length=16, data=command)
            dali.connection.write(frame)
            answer = False
            try:
                while not answer:
                    frame = dali.connection.read_raw_frame(dali.timeout_sec)
                    if frame.data == cmd_frame.data:
                        continue
                    if frame.length == 8 and frame.data == 0xFF:
                        click.echo(f"A{short_address:02}")
            except Empty:
                pass
