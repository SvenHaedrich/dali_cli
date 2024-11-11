"""Control gear special commands implemenatation."""

import click
import dali

from .opcode import SpecialCommandOpcode
from .action import write_gear_frame, write_frame_and_show_answer


@click.command(name="term", help="Terminate initialisation and identifaction states.")
def term():
    write_gear_frame(SpecialCommandOpcode.TERMINATE)


@click.command(name="dtr0", help="Set data transfer register 0.")
@click.argument("data", type=click.INT)
def dtr0(data):
    if 0 <= data < dali.MAX_VALUE:
        write_gear_frame(SpecialCommandOpcode.DTR0, data)
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
    write_gear_frame(SpecialCommandOpcode.INITIALISE, data, True)


@click.command(name="rand", help="Generate new randomAddress.")
def rand():
    write_gear_frame(SpecialCommandOpcode.RANDOMISE, send_twice=True)


@click.command(name="comp", help="Compare searchAddress and randomAddress.")
def comp():
    write_frame_and_show_answer(SpecialCommandOpcode.COMPARE)


@click.command(name="withdraw", help="Withdraw from initialisation state.")
def withdraw():
    write_gear_frame(SpecialCommandOpcode.WIDTHDRAW)


@click.command(name="ping", help="Indicate presence.")
def ping():
    write_gear_frame(SpecialCommandOpcode.PING)


@click.command(name="search", help="Set searchAddress.")
@click.argument("address", type=click.INT)
def search(address):
    if 0 <= address < 0x1000000:
        write_gear_frame(SpecialCommandOpcode.SEARCHADDRH, (address >> 16) & 0xFF)
        while True:
            dali.connection.get(timeout=dali.timeout_sec)
            if dali.connection.data == dali.connection.last_transmit:
                break
            write_gear_frame(SpecialCommandOpcode.SEARCHADDRM, (address >> 8) & 0xFF)
        while True:
            dali.connection.get(timeout=dali.timeout_sec)
            if dali.connection.data == dali.connection.last_transmit:
                break
        write_gear_frame(SpecialCommandOpcode.SEARCHADDRL, (address >> 8) & 0xFF)
        while True:
            dali.connection.get(timeout=dali.timeout_sec)
            if dali.connection.data == dali.connection.last_transmit:
                break
    else:
        raise click.BadParameter(
            "needs to be between 0 and 16777215.", param_hint="ADDRESS"
        )


@click.command(name="program", help="Program shortAddress.")
@click.argument("address", type=click.INT)
def program(address):
    if 0 <= address < dali.MAX_ADR:
        write_gear_frame(
            SpecialCommandOpcode.PROGRAM_SHORT_ADDRESS, ((address << 1) | 1)
        )
    elif address == 0xFF:
        write_gear_frame(SpecialCommandOpcode.PROGRAM_SHORT_ADDRESS, 0xFF)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_ADR-1}.", param_hint="ADDRESS"
        )


@click.command(name="verify", help="Verify shortAddress.")
@click.argument("address", type=click.INT)
def verify(address):
    if 0 <= address < dali.MAX_ADR:
        write_frame_and_show_answer(
            SpecialCommandOpcode.VERIFY_SHORT_ADDRESS, ((address << 1) | 1)
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_ADR-1}.", param_hint="ADDRESS"
        )


@click.command(name="short", help="Query shortAddress.")
def short(address):
    write_frame_and_show_answer(SpecialCommandOpcode.QUERY_SHORT_ADDRESS)


@click.command(name="dt", help="Enable device type.")
@click.argument("type", type=click.INT)
def dt(type):
    if 0 <= type < dali.MAX_VALUE:
        write_gear_frame(SpecialCommandOpcode.ENABLE_DEVICE_TYPE, type)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="TYPE"
        )


@click.command(name="dtr1", help="Set data transfer register 1.")
@click.argument("data", type=click.INT)
def dtr1(data):
    if 0 <= data < dali.MAX_VALUE:
        write_gear_frame(SpecialCommandOpcode.DTR1, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )


@click.command(name="dtr2", help="Set data transfer register 2.")
@click.argument("data", type=click.INT)
def dtr2(data):
    if 0 <= data < dali.MAX_VALUE:
        write_gear_frame(SpecialCommandOpcode.DTR2, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )


@click.command(name="write", help="Write data into memory bank.")
@click.argument("data", type=click.INT)
def write(data):
    if 0 <= data < dali.MAX_VALUE:
        write_frame_and_show_answer(SpecialCommandOpcode.WRITE, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )


@click.command(name="noreply", help="Write data into memory bank. No reply to command")
@click.argument("data", type=click.INT)
def noreply(data):
    if 0 <= data < dali.MAX_VALUE:
        write_gear_frame(SpecialCommandOpcode.WRITE_NR, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {dali.MAX_VALUE-1}.", param_hint="DATA"
        )
