from queue import Empty
import click
import dali

from .opcode import SpecialCommandOpcodes
from ..frame import DaliTxFrame


def write_gear_frame(address_byte, opcode_byte=0, send_twice=False):
    command = address_byte << 8 | opcode_byte
    frame = DaliTxFrame(length=16, data=command, send_twice=send_twice)
    dali.connection.write(frame)
    return frame


def write_frame_and_show_answer(address_byte, opcode_byte=0):
    dali.connection.start_read()
    cmd_frame = write_gear_frame(address_byte, opcode_byte)
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


@click.command(name="term", help="Terminate initialisation and identifaction states.")
def term():
    write_gear_frame(SpecialCommandOpcodes.TERMINATE)


@click.command(name="dtr0", help="Set data transfer register 0.")
@click.argument("data", type=click.INT)
def dtr0(data):
    if data in range(dali.MAX_VALUE):
        write_gear_frame(SpecialCommandOpcodes.DTR0, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )


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
            if int(device) in range(dali.MAX_ADR):
                data = (int(device) << 1) + 1
    except ValueError:
        raise click.BadParameter("use ALL, UN or short address", param_hint="DEVICE")
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
    if address in range(0x1000000):
        dali.connection.start_read()
        cmd_frame = write_gear_frame(
            SpecialCommandOpcodes.SEARCHADDRH, (address >> 16) & 0xFF
        )
        while True:
            readback = dali.connection.read_raw_frame(timeout=dali.timeout_sec)
            if cmd_frame.data == readback.data:
                break
        cmd_frame = write_gear_frame(
            SpecialCommandOpcodes.SEARCHADDRM, (address >> 8) & 0xFF
        )
        while True:
            readback = dali.connection.read_raw_frame(timeout=dali.timeout_sec)
            if cmd_frame.data == readback.data:
                break
        cmd_frame = write_gear_frame(
            SpecialCommandOpcodes.SEARCHADDRL, (address >> 8) & 0xFF
        )
        while True:
            readback = dali.connection.read_raw_frame(timeout=dali.timeout_sec)
            if cmd_frame.data == readback.data:
                break
    else:
        raise click.BadParameter(
            "needs to be between 0 and 16777215.", param_hint="ADDRESS"
        )


@click.command(name="program", help="Program shortAddress.")
@click.argument("address", type=click.INT)
def program(address):
    if address in range(dali.MAX_ADR):
        write_gear_frame(
            SpecialCommandOpcodes.PROGRAM_SHORT_ADDRESS, ((address << 1) | 1)
        )
    elif address == 0xFF:
        write_gear_frame(SpecialCommandOpcodes.PROGRAM_SHORT_ADDRESS, 0xFF)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_ADR-1}.", param_hint="ADDRESS"
        )


@click.command(name="verify", help="Verify shortAddress.")
@click.argument("address", type=click.INT)
def verify(address):
    if address in range(dali.MAX_ADR):
        write_frame_and_show_answer(
            SpecialCommandOpcodes.VERIFY_SHORT_ADDRESS, ((address << 1) | 1)
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_ADR-1}.", param_hint="ADDRESS"
        )


@click.command(name="short", help="Query shortAddress.")
def short(address):
    write_frame_and_show_answer(SpecialCommandOpcodes.QUERY_SHORT_ADDRESS)


@click.command(name="dt", help="Enable device type.")
@click.argument("type", type=click.INT)
def dt(type):
    if type in range(dali.MAX_VALUE):
        write_gear_frame(SpecialCommandOpcodes.ENABLE_DEVICE_TYPE, type)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="TYPE"
        )


@click.command(name="dtr1", help="Set data transfer register 1.")
@click.argument("data", type=click.INT)
def dtr1(data):
    if data in range(dali.MAX_VALUE):
        write_gear_frame(SpecialCommandOpcodes.DTR1, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )


@click.command(name="dtr2", help="Set data transfer register 2.")
@click.argument("data", type=click.INT)
def dtr2(data):
    if data in range(dali.MAX_VALUE):
        write_gear_frame(SpecialCommandOpcodes.DTR2, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )


@click.command(name="write", help="Write data into memory bank.")
@click.argument("data", type=click.INT)
def write(data):
    if data in range(dali.MAX_VALUE):
        write_frame_and_show_answer(SpecialCommandOpcodes.WRITE, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )


@click.command(name="noreply", help="Write data into memory bank. No reply to command")
@click.argument("data", type=click.INT)
def noreply(data):
    if data in range(dali.MAX_VALUE):
        write_gear_frame(SpecialCommandOpcodes.WRITE_NR, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )
