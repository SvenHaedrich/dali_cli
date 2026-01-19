"""Control device discovery and enumerate."""

import click
from dali_interface import DaliFrame, DaliInterface

from ..device.device_opcode import DeviceSpecialCommandOpcode
from ..system.constants import DaliFrameLength, DaliMax
from .gear_action import set_gear_dtr0, write_gear_frame, write_gear_frame_and_wait
from .gear_address import GearAddress
from .gear_opcode import GearConfigureCommandOpcode, GearSpecialCommandOpcode


def prepare_bus(dali: DaliInterface) -> None:
    # INITIALISE ALL
    write_gear_frame_and_wait(dali, GearSpecialCommandOpcode.INITIALISE, 0xFF, True)


def clear_short_addresses(dali: DaliInterface) -> None:
    set_gear_dtr0(dali, 0xFF)
    address = GearAddress()
    address.broadcast()
    write_gear_frame_and_wait(
        dali, address.byte, GearConfigureCommandOpcode.SET_SHORT_ADDRESS, True
    )


def remove_from_all_groups(dali: DaliInterface) -> None:
    for group in range(DaliMax.GEAR_GROUP):
        address = GearAddress()
        address.broadcast()
        write_gear_frame_and_wait(
            dali, address.byte, GearConfigureCommandOpcode.REMOVE_GROUP + group, True
        )


def request_new_random_addresses(dali: DaliInterface) -> None:
    write_gear_frame(dali, GearSpecialCommandOpcode.RANDOMISE, send_twice=True)


def set_search_address(dali: DaliInterface, search: int) -> None:
    if 0 <= search < 0x1000000:
        write_gear_frame_and_wait(
            dali, GearSpecialCommandOpcode.SEARCHADDRH, (search >> 16) & 0xFF
        )
        write_gear_frame_and_wait(
            dali, GearSpecialCommandOpcode.SEARCHADDRM, (search >> 8) & 0xFF
        )
        write_gear_frame_and_wait(
            dali, GearSpecialCommandOpcode.SEARCHADDRL, search & 0xFF
        )


def compare(dali: DaliInterface) -> bool:
    data = GearSpecialCommandOpcode.COMPARE << 8
    result = dali.query_reply(DaliFrame(length=DaliFrameLength.GEAR, data=data))
    return result.length == DaliFrameLength.BACKWARD


def binary_search(dali: DaliInterface) -> int | None:
    search = DaliMax.RANDOM_ADR - 1
    set_search_address(dali, search)
    if compare(dali):
        position = 23
        while position >= 0:
            set_search_address(dali, search & ~(1 << position))
            if compare(dali):
                search = search & ~(1 << position)
            position = position - 1
        return search
    click.echo("No (more) gears.")
    return None


def set_short_address(dali: DaliInterface, new_short_address: int) -> bool:
    write_gear_frame(
        dali,
        GearSpecialCommandOpcode.PROGRAM_SHORT_ADDRESS,
        ((new_short_address << 1) | 1),
    )
    data = (GearSpecialCommandOpcode.VERIFY_SHORT_ADDRESS << 8) | ((new_short_address << 1) | 1)
    result = dali.query_reply(DaliFrame(length=DaliFrameLength.GEAR, data=data))
    if result.length == DaliFrameLength.BACKWARD:
        write_gear_frame(dali, GearSpecialCommandOpcode.WITHDRAW)
        return True
    return False


def finish_work(dali: DaliInterface) -> None:
    write_gear_frame(dali, GearSpecialCommandOpcode.TERMINATE)


@click.command(
    name="enum", help="Clear and re-program short addresses of all control gears."
)
@click.pass_obj
def gear_enumerate(dali: DaliInterface):
    prepare_bus(dali)
    clear_short_addresses(dali)
    remove_from_all_groups(dali)
    request_new_random_addresses(dali)
    next_short_address = 0
    while True:
        search = binary_search(dali)
        if search is None:
            break
        set_search_address(dali, search)
        if set_short_address(dali, next_short_address):
            click.echo(f"assigned D{next_short_address:02}.")
            next_short_address = next_short_address + 1
        else:
            click.echo("address search failed.")
    finish_work(dali)
