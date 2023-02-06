from queue import Empty
from DALI.forward_frame_16bit import ForwardFrame16Bit
from DALI.address_byte import DALIAddressByte
from DALI.raw_frame import Raw_Frame

import click
import dali


def simple_level_command(adr, mnemonic):
    address = DALIAddressByte()
    address.arg(adr)
    opcode = ForwardFrame16Bit.opcode(mnemonic)
    command = address.byte << 8 | opcode
    frame = Raw_Frame(length=16, data=command)
    dali.connection.write(frame)


@click.command(name="off", help="Lights off.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def off(adr):
    simple_level_command(adr, "off")


@click.command(name="up", help="Dim up.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def up(adr):
    simple_level_command(adr, "up")


@click.command(name="down", help="Dim down.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def down(adr):
    simple_level_command(adr, "down")


@click.command(name="max", help="Recall maximum.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def max(adr):
    simple_level_command(adr, "recall max level")


@click.command(name="min", help="Recall minimum.")
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def min(adr):
    simple_level_command(adr, "recall min level")


@click.command(name="dapc", help="Direct arc power control (dim level).")
@click.argument("level", type=click.INT)
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def dapc(adr, level):
    if level in range(0x100):
        address = DALIAddressByte(dapc=True)
        address.arg(adr)
        command = address.byte << 8 | level
        frame = Raw_Frame(length=16, data=command)
        dali.connection.write(frame)


@click.command(name="goto", help="Go to scene.")
@click.argument("scene", type=click.INT)
@click.option(
    "--adr",
    default="BC",
    help="Address, can be a short address (A0..A63) or group address (G0..G15).",
)
def goto(adr, scene):
    address = DALIAddressByte()
    address.arg(adr)
    opcode = ForwardFrame16Bit.opcode(f"GO TO SCENE {scene}")
    command = address.byte << 8 | opcode
    frame = Raw_Frame(length=16, data=command)
    dali.connection.write(frame)
