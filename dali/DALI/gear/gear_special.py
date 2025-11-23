"""Control gear special commands implementation."""

import click
from dali_interface import DaliInterface

from ..system.constants import DaliMax
from .gear_action import (
    write_frame_and_show_answer,
    write_gear_frame,
    write_gear_frame_and_wait,
)
from .gear_opcode import GearSpecialCommandOpcode


@click.command(name="term", help="Terminate initialisation and identification states.")
@click.pass_obj
def term(ctx: DaliInterface):
    write_gear_frame(ctx, GearSpecialCommandOpcode.TERMINATE)


@click.command(name="dtr0", help="Set data transfer register 0.")
@click.pass_obj
@click.argument("data", type=click.INT)
def dtr0(ctx: DaliInterface, data):
    if 0 <= data < DaliMax.VALUE:
        write_gear_frame(ctx, GearSpecialCommandOpcode.DTR0, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE - 1}.", param_hint="DATA"
        )


@click.command(
    name="init", help="Enable initialisation mode. Argument device=(ALL|UN|0..63)"
)
@click.pass_obj
@click.argument("device", type=click.STRING)
def init(ctx: DaliInterface, device):
    try:
        if device.upper() == "ALL":
            data = 0x00
        elif device.upper() == "UN":
            data = 0xFF
        else:
            if int(device) in range(DaliMax.ADR):
                data = (int(device) << 1) + 1
            else:
                raise ValueError
        write_gear_frame(ctx, GearSpecialCommandOpcode.INITIALISE, data, True)
    except ValueError as error:
        raise click.BadParameter(
            "use ALL, UN or valid short address", param_hint="DEVICE"
        ) from error


@click.command(name="rand", help="Generate new randomAddress.")
@click.pass_obj
def rand(ctx: DaliInterface):
    write_gear_frame(ctx, GearSpecialCommandOpcode.RANDOMISE, send_twice=True)


@click.command(name="comp", help="Compare searchAddress and randomAddress.")
@click.pass_obj
def comp(ctx: DaliInterface):
    write_frame_and_show_answer(ctx, GearSpecialCommandOpcode.COMPARE)


@click.command(name="withdraw", help="Withdraw from initialisation state.")
@click.pass_obj
def withdraw(ctx: DaliInterface):
    write_gear_frame(ctx, GearSpecialCommandOpcode.WITHDRAW)


@click.command(name="ping", help="Indicate presence.")
@click.pass_obj
def ping(ctx: DaliInterface):
    write_gear_frame(ctx, GearSpecialCommandOpcode.PING)


@click.command(name="search", help="Set searchAddress.")
@click.pass_obj
@click.argument("address", type=click.INT)
def search(ctx: DaliInterface, address):
    if 0 <= address < 0x1000000:
        write_gear_frame_and_wait(
            ctx, GearSpecialCommandOpcode.SEARCHADDRH, (address >> 16) & 0xFF
        )
        write_gear_frame_and_wait(
            ctx, GearSpecialCommandOpcode.SEARCHADDRM, (address >> 8) & 0xFF
        )
        write_gear_frame_and_wait(
            ctx, GearSpecialCommandOpcode.SEARCHADDRL, address & 0xFF
        )
    else:
        raise click.BadParameter(
            "needs to be between 0 and 16777215.", param_hint="ADDRESS"
        )


@click.command(name="program", help="Program shortAddress.")
@click.pass_obj
@click.argument("address", type=click.INT)
def program(ctx: DaliInterface, address):
    if 0 <= address < DaliMax.ADR:
        write_gear_frame(
            ctx, GearSpecialCommandOpcode.PROGRAM_SHORT_ADDRESS, ((address << 1) | 1)
        )
    elif address == 0xFF:
        write_gear_frame(ctx, GearSpecialCommandOpcode.PROGRAM_SHORT_ADDRESS, 0xFF)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.ADR - 1}.", param_hint="ADDRESS"
        )


@click.command(name="verify", help="Verify shortAddress.")
@click.pass_obj
@click.argument("address", type=click.INT)
def verify(ctx: DaliInterface, address):
    if 0 <= address < DaliMax.ADR:
        write_frame_and_show_answer(
            ctx, GearSpecialCommandOpcode.VERIFY_SHORT_ADDRESS, ((address << 1) | 1)
        )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.ADR - 1}.", param_hint="ADDRESS"
        )


@click.command(name="short", help="Query shortAddress.")
@click.pass_obj
def short(dali: DaliInterface):
    write_frame_and_show_answer(dali, GearSpecialCommandOpcode.QUERY_SHORT_ADDRESS)


@click.command(name="dt", help="Enable device type.")
@click.pass_obj
@click.argument("devicetype", type=click.INT)
def dt(ctx: DaliInterface, devicetype):
    if 0 <= devicetype < DaliMax.VALUE:
        write_gear_frame(ctx, GearSpecialCommandOpcode.ENABLE_DEVICE_TYPE, devicetype)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE - 1}.", param_hint="DEVICETYPE"
        )


@click.command(name="dtr1", help="Set data transfer register 1.")
@click.pass_obj
@click.argument("data", type=click.INT)
def dtr1(ctx: DaliInterface, data):
    if 0 <= data < DaliMax.VALUE:
        write_gear_frame(ctx, GearSpecialCommandOpcode.DTR1, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE - 1}.", param_hint="DATA"
        )


@click.command(name="dtr2", help="Set data transfer register 2.")
@click.pass_obj
@click.argument("data", type=click.INT)
def dtr2(ctx: DaliInterface, data):
    if 0 <= data < DaliMax.VALUE:
        write_gear_frame(ctx, GearSpecialCommandOpcode.DTR2, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE - 1}.", param_hint="DATA"
        )


@click.command(name="write", help="Write data into memory bank.")
@click.pass_obj
@click.argument("data", type=click.INT)
def write(ctx: DaliInterface, data):
    if 0 <= data < DaliMax.VALUE:
        write_frame_and_show_answer(ctx, GearSpecialCommandOpcode.WRITE, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE - 1}.", param_hint="DATA"
        )


@click.command(name="noreply", help="Write data into memory bank. No reply to command")
@click.pass_obj
@click.argument("data", type=click.INT)
def noreply(ctx: DaliInterface, data):
    if 0 <= data < DaliMax.VALUE:
        write_gear_frame(ctx, GearSpecialCommandOpcode.WRITE_NR, data)
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.VALUE - 1}.", param_hint="DATA"
        )
