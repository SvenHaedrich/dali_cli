from queue import Empty
from DALI.forward_frame_16bit import ForwardFrame16Bit
from DALI.address_byte import DALIAddressByte
from DALI.raw_frame import Raw_Frame

import click
import dali


class SpecialCommandOpcodes:
    TERMINATE = 0xA1
    DTR0 = 0xA3
    INITIALISE = 0xA5
    RANDOMISE = 0xA7
    COMPARE = 0xA9
    WIDTHDRAW = 0xAB
    PING = 0xAD
    SEARCHADDRH = 0xB1
    SEARCHADDRM = 0xB3
    SEARCHADDRL = 0xB5
    PROGRAM_SHORT_ADDRESS = 0xB7
    VERIFY_SHORT_ADDRESS = 0xB9
    QUERY_SHORT_ADDRESS = 0xBB
    ENABLE_DEVICE_TYPE = 0xC1
    DTR1 = 0xC3
    DTR2 = 0xC5
    WRITE = 0xC7
    WRITE_NR = 0xC9


def write_gear_frame(address_byte, opcode_byte=0, send_twice=False):
    command = address_byte << 8 | opcode_byte
    frame = Raw_Frame(length=16, data=command, send_twice=send_twice)
    dali.connection.write(frame)


def write_frame_and_show_answer(address_byte, opcode_byte=0):
    dali.connection.start_read()
    command = address_byte << 8 | opcode_byte
    cmd_frame = Raw_Frame(length=16, data=command)
    dali.connection.write(cmd_frame)
    answer = False
    try:
        while not answer:
            frame = dali.connection.read_raw_frame(dali.timeout_sec)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                answer = True
                click.echo(f"{frame.data} = 0x{frame.data:02X} = {frame.data:08b}b")
    except Empty:
        if not answer:
            click.echo("timeout - NO")
    dali.connection.close()


@click.command(name="term", help="Terminate initialisation and identifaction states.")
def term():
    write_gear_frame(SpecialCommandOpcodes.TERMINATE)


@click.command(name="dtr0", help="Set data transfer register 0.")
@click.argument("data", type=click.INT)
def dtr0(data):
    if data in range(0, 0x100):
        write_gear_frame(SpecialCommandOpcodes.DTR0, data)
    else:
        click.echo("{data} - invalid data to DTR0")


@click.command(
    name="init", help="Enable initialisation mode. Argument device=(ALL|UN|0..63)"
)
@click.argument("device", type=click.STRING)
def init(device):
    try:
        if device.upper() == "ALL":
            data = 0x00
        elif device.upper() == "UN":
            data = 0xFF
        else:
            if int(device) in range(0, 0x40):
                data = (int(device) << 1) + 1
    except ValueError:
        click.echo("Invalide device for INITIALISE")
        return
    write_gear_frame(SpecialCommandOpcodes.INITIALISE, data, True)


@click.command(name="rand", help="Generate new randomAddress.")
def rand():
    write_gear_frame(SpecialCommandOpcodes.RANDOMISE, send_twice=True)


@click.command(name="comp", help="Compare searchAddress and randomAddress.")
def comp():
    write_frame_and_show_answer(SpecialCommandOpcodes.COMPARE)


@click.command(name="withdraw", help="Withdraw from initialisation state.")
def withdraw():
    write_gear_frame(SpecialCommandOpcodes.WIDTHDRAW)


@click.command(name="ping", help="Indicate presence.")
def ping():
    write_gear_frame(SpecialCommandOpcodes.PING)


@click.command(name="search", help="Set searchAddress.")
@click.argument("address", type=click.INT)
def search(address):
    if address in range(0, 0x1000000):
        dali.connection.start_read()
        command = SpecialCommandOpcodes.SEARCHADDRH << 8 | (address >> 16) & 0xFF
        frame = Raw_Frame(length=16, data=command)
        dali.connection.write(frame)
        while True:
            readback = dali.connection.read_raw_frame(timeout=dali.timeout_sec)
            if command_frame.data == readback.data:
                break
        command = SpecialCommandOpcodes.SEARCHADDRM << 8 | (address >> 8) & 0xFF
        frame = Raw_Frame(length=16, data=command)
        dali.connection.write(frame)
        while True:
            readback = dali.connection.read_raw_frame(timeout=dali.timeout_sec)
            if command_frame.data == readback.data:
                break
        command = SpecialCommandOpcodes.SEARCHADDRL << 8 | address & 0xFF
        frame = Raw_Frame(length=16, data=command)
        dali.connection.write(frame)
        while True:
            readback = dali.connection.read_raw_frame(timeout=dali.timeout_sec)
            if command_frame.data == readback.data:
                break
    else:
        click.echo(f"{address}: Invalid address for searchAddress.")


@click.command(name="program", help="Program shortAddress.")
@click.argument("address", type=click.INT)
def program(address):
    if address in range(0, 0x40):
        write_gear_frame(
            SpecialCommandOpcodes.PROGRAM_SHORT_ADDRESS, ((address << 1) | 1)
        )
    elif address == 0xFF:
        write_gear_frame(SpecialCommandOpcodes.PROGRAM_SHORT_ADDRESS, 0xFF)
    else:
        click.echo(f"{address}: Invalid address for shortAddress.")


@click.command(name="verify", help="Verify shortAddress.")
@click.argument("address", type=click.INT)
def verify(address):
    if address in range(0, 0x40):
        write_frame_and_show_answer(
            SpecialCommandOpcodes.VERIFY_SHORT_ADDRESS, ((address << 1) | 1)
        )
    else:
        click.echo(f"{address}: Invalid address for shortAddress.")


@click.command(name="short", help="Query shortAddress.")
def short(address):
    write_frame_and_show_answer(SpecialCommandOpcodes.QUERY_SHORT_ADDRESS)


@click.command(name="dt", help="Enable device type.")
@click.argument("type", type=click.INT)
def dt(type):
    if type in range(0, 0x100):
        write_gear_frame(SpecialCommandOpcodes.ENABLE_DEVICE_TYPE, type)
    else:
        click.echo(f"{type} - invalid type to ENABLE DEVICE TYPE")


@click.command(name="dtr1", help="Set data transfer register 1.")
@click.argument("data", type=click.INT)
def dtr1(data):
    if data in range(0, 0x100):
        write_gear_frame(SpecialCommandOpcodes.DTR1, data)
    else:
        click.echo(f"{data} - invalid data to DTR1")


@click.command(name="dtr2", help="Set data transfer register 2.")
@click.argument("data", type=click.INT)
def dtr2(data):
    if data in range(0, 0x100):
        write_gear_frame(SpecialCommandOpcodes.DTR2, data)
    else:
        click.echo(f"{data} - invalid data to DTR2")


@click.command(name="write", help="Write data into memory bank.")
@click.argument("data", type=click.INT)
def write(data):
    if data in range(0, 0x100):
        write_frame_and_show_answer(SpecialCommandOpcodes.WRITE, data)
    else:
        click.echo(f"{data} - invalid data to WRITE MEMORY LOCATION")


@click.command(name="noreply", help="Write data into memory bank. No reply to command")
@click.argument("data", type=click.INT)
def noreply(data):
    if data in range(0, 0x100):
        write_gear_frame(SpecialCommandOpcodes.WRITE_NR, data)
    else:
        click.echo(f"{data} - invalid data to WRITE MEMORY LOCATION - NO REPLY")
