from queue import Empty
from DALI.forward_frame_16bit import ForwardFrame16Bit
from DALI.address_byte import DALIAddressByte
from DALI.raw_frame import Raw_Frame

import click
import dali
import time


def simple_configure_command(adr, mnemonic, send_twice=False):
    address = DALIAddressByte()
    address.arg(adr)
    opcode = ForwardFrame16Bit.opcode(mnemonic)
    command = address.byte << 8 | opcode
    frame = Raw_Frame(length=16, data=command)
    dali.connection.write(frame)


def set_dtr0(value):
    if value in range(0, 0x100):
        dali.connection.start_read()
        command = 0xA3 << 8 | value
        command_frame = Raw_Frame(length=16, data=command)
        dali.connection.write(command_frame)
        while True:
            readback = dali.connection.read_raw_frame(timeout=dali.timeout_sec)
            if command_frame.data == readback.data:
                return


@click.command(
    name="reset", help="Reset all control gear variables to their reset value."
)
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def reset(adr):
    simple_configure_command(adr, "RESET", True)


@click.command(name="actual", help="Store the actualLevel into DTR0.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def actual(adr):
    simple_configure_command(adr, "STORE ACTUAL LEVEL IN DTR0", True)


@click.command(name="op", help="Set operating mode.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("mode", type=click.INT)
def op(adr, mode):
    set_dtr0(mode)
    simple_configure_command(adr, "SET OPERATING MODE (DTR0)", True)
    dali.connection.close()


@click.command(name="reset_mem", help="Reset memory bank to reset value.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("bank", type=click.INT)
def reset_mem(adr, bank):
    set_dtr0(bank)
    simple_configure_command(adr, "RESET MEMORY BANK (DTR0)", True)
    dali.connection.close()


@click.command(name="id", help="Identify device.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def id(adr):
    simple_configure_command(adr, "IDENTIFY DEVICE", True)


@click.command(name="max", help="Set maximum level.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("level", type=click.INT)
def max(adr, level):
    set_dtr0(level)
    simple_configure_command(adr, "SET MAX LEVEL (DTR0)", True)
    dali.connection.close()


@click.command(name="min", help="Set minimum level.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("level", type=click.INT)
def min(adr, level):
    set_dtr0(level)
    simple_configure_command(adr, "SET MIN LEVEL (DTR0)", True)
    dali.connection.close()


@click.command(name="fail", help="Set system failure level.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("level", type=click.INT)
def fail(adr, level):
    set_dtr0(level)
    simple_configure_command(adr, "SET SYSTEM FAILURE LEVEL (DTR0)", True)
    dali.connection.close()


@click.command(name="on", help="Set power on level.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("level", type=click.INT)
def on(adr, level):
    set_dtr0(level)
    simple_configure_command(adr, "SET POWER ON LEVEL (DTR0)", True)
    dali.connection.close()


@click.command(name="time", help="Set fade time.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("value", type=click.INT)
def time(adr, value):
    set_dtr0(value)
    simple_configure_command(adr, "SET FADE TIME (DTR0)", True)
    dali.connection.close()


@click.command(name="rate", help="Set fade rate.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("value", type=click.INT)
def rate(adr, value):
    set_dtr0(value)
    simple_configure_command(adr, "SET FADE RATE (DTR0)", True)
    dali.connection.close()


@click.command(name="ext", help="Set extended fade time.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("value", type=click.INT)
def ext(adr, value):
    set_dtr0(value)
    simple_configure_command(adr, "SET EXTENDED FADE TIME (DTR0)", True)
    dali.connection.close()


@click.command(name="scene", help="Set scene to level.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("number", type=click.INT)
@click.argument("level", type=click.INT)
def scene(adr, number, level):
    if number in range(0, 0x10):
        set_dtr0(level)
        simple_configure_command(adr, f"SET SCENE (DTR0) {number}", True)
        dali.connection.close()


@click.command(name="remove", help="Remove from scene.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("number", type=click.INT)
def remove(adr, number):
    if number in range(0, 0x10):
        simple_configure_command(adr, f"REMOVE FROM SCENE {number}", True)


@click.command(name="add", help="Add to group.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("group", type=click.INT)
def add(adr, group):
    if group in range(0, 0x10):
        simple_configure_command(adr, f"ADD TO GROUP {group}", True)


@click.command(name="ungroup", help="Remove from group.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("group", type=click.INT)
def ungroup(adr, group):
    if group in range(0, 0x10):
        simple_configure_command(adr, f"REMOVE FROM GROUP {group}", True)


@click.command(name="short", help="Set short address.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
@click.argument("address", type=click.INT)
def short(adr, address):
    if address in range(0, 0x40):
        set_dtr0(level)
        simple_configure_command(adr, "SET SHORT ADDRESS (DTR0)", True)
        dali.connection.close()


@click.command(name="enable", help="Enable write access.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def enable(adr):
    simple_configure_command(adr, "ENABLE WRITE MEMORY", True)
