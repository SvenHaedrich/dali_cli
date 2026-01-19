"""Control device discovery and enumerate."""

import click
from dali_interface import DaliFrame, DaliInterface

from ..system.constants import DaliFrameLength, DaliMax
from .device_action import set_device_dtr0, set_device_dtr2_dtr1
from .device_address import DeviceAddress, InstanceAddress
from .device_opcode import DeviceConfigureCommandOpcode, DeviceSpecialCommandOpcode


def prepare_bus(dali: DaliInterface) -> None:
    address = DeviceAddress("SPECIAL")
    data = address.byte << 16 | DeviceSpecialCommandOpcode.INITIALISE << 8 | 0xFF
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data, send_twice=True), block=True)
    address = DeviceAddress()
    instance = InstanceAddress()
    data = address.byte << 16 | instance.byte << 8 | DeviceConfigureCommandOpcode.START_QUIESCENT_MODE
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data, send_twice=True), block=True)


def clear_short_addresses(dali: DaliInterface) -> None:
    set_device_dtr0(dali, 0xFF)
    address = DeviceAddress()
    instance = InstanceAddress()
    instance.device()
    data = address.byte << 16 | instance.byte << 8 | DeviceConfigureCommandOpcode.SET_SHORT_ADDRESS
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data, send_twice=True), block=True)


def remove_from_all_groups(dali: DaliInterface) -> None:
    set_device_dtr2_dtr1(dali, 0xFF, 0xFF)
    address = DeviceAddress()
    instance = InstanceAddress()
    instance.device()
    data = address.byte << 16 | instance.byte << 8 | DeviceConfigureCommandOpcode.REMOVE_FROM_DEVICE_GROUPS_0_15
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data, send_twice=True))
    data = address.byte << 16 | instance.byte << 8 | DeviceConfigureCommandOpcode.REMOVE_FROM_DEVICE_GROUPS_16_31
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data, send_twice=True))


def request_new_random_addresses(dali: DaliInterface) -> None:
    address = DeviceAddress("SPECIAL")
    data = address.byte << 16 | DeviceSpecialCommandOpcode.RANDOMISE << 8
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data, send_twice=True), block=True)


def set_search_address(dali: DaliInterface, search: int) -> None:
    address = DeviceAddress("SPECIAL")
    data = address.byte << 16 | DeviceSpecialCommandOpcode.SEARCHADDRL << 8 | search & 0xFF
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data), block=True)
    search = search >> 8
    data = address.byte << 16 | DeviceSpecialCommandOpcode.SEARCHADDRM << 8 | search & 0xFF
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data), block=True)
    search = search >> 8
    data = address.byte << 16 | DeviceSpecialCommandOpcode.SEARCHADDRH << 8 | search & 0xFF
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data), block=True)


def compare(dali: DaliInterface) -> bool:
    address = DeviceAddress("SPECIAL")
    data = address.byte << 16 | DeviceSpecialCommandOpcode.COMPARE << 8
    result = dali.query_reply(DaliFrame(length=DaliFrameLength.DEVICE, data=data))
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
    click.echo("No (more) devices.")
    return None


def set_short_address(dali: DaliInterface, new_short_address: int) -> bool:
    address = DeviceAddress("SPECIAL")
    data = address.byte << 16 | DeviceSpecialCommandOpcode.PROGRAM_SHORT_ADDRESS << 8 | new_short_address & 0xFF
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data), block=True)
    data = address.byte << 16 | DeviceSpecialCommandOpcode.VERIFY_SHORT_ADDRESS << 8 | new_short_address & 0xFF
    result = dali.query_reply(DaliFrame(length=DaliFrameLength.DEVICE, data=data))
    if result.length == DaliFrameLength.BACKWARD:
        data = address.byte << 16 | DeviceSpecialCommandOpcode.WITHDRAW << 8
        dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data), block=True)
        return True
    return False


def finish_work(dali: DaliInterface) -> None:
    address = DeviceAddress("SPECIAL")
    data = address.byte << 16 | DeviceSpecialCommandOpcode.TERMINATE << 8
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data), block=True)
    address = DeviceAddress()
    instance = InstanceAddress()
    data = address.byte << 16 | instance.byte << 8 | DeviceConfigureCommandOpcode.STOP_QUIESCENT_MODE
    dali.transmit(DaliFrame(length=DaliFrameLength.DEVICE, data=data, send_twice=True), block=True)


@click.command(name="enum", help="Clear and re-program short addresses of all control devices.")
@click.pass_obj
def device_enumerate(dali: DaliInterface):
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
