"""Control device configure commands implementation."""

import click

from ..dali_interface.dali_interface import DaliInterface
from ..system.constants import DaliMax
from .device_action import set_device_dtr0, set_device_dtr2_dtr1, write_device_frame
from .device_address import DeviceAddress, InstanceAddress
from .device_opcode import DeviceConfigureCommandOpcode

device_address_option = click.option(
    "--adr",
    default="BC",
    help="Address, can be short address (0..63), group address (G0..G15), broadcast BC, or unaddressed BCU",
)


@click.command(name="start", help="Start quiescent mode.")
@click.pass_obj
@device_address_option
def start(dali: DaliInterface, adr: str):
    address = DeviceAddress(adr)
    instance = InstanceAddress()
    if address.isvalid():
        write_device_frame(
            dali,
            address.byte,
            instance.byte,
            DeviceConfigureCommandOpcode.START_QUIESCENT_MODE,
            True,
        )


@click.command(name="stop", help="Stop quiescent mode.")
@click.pass_obj
@device_address_option
def stop(dali: DaliInterface, adr: str):
    address = DeviceAddress(adr)
    instance = InstanceAddress()
    if address.isvalid():
        write_device_frame(
            dali,
            address.byte,
            instance.byte,
            DeviceConfigureCommandOpcode.STOP_QUIESCENT_MODE,
            True,
        )


@click.command(name="reset", help="Reset all variables.")
@click.pass_obj
@device_address_option
def reset(dali: DaliInterface, adr: str):
    address = DeviceAddress(adr)
    instance = InstanceAddress()
    if address.isvalid():
        write_device_frame(
            dali,
            address.byte,
            instance.byte,
            DeviceConfigureCommandOpcode.RESET,
            True,
        )


@click.command(name="short", help="Set short address to ADDRESS.")
@click.pass_obj
@device_address_option
@click.argument("address", type=click.INT)
def short(dali, adr, address):
    if 0 <= address < DaliMax.ADR:
        address = (address * 2) + 1
    elif address != 255:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.ADR-1}", param_hint="ADDRESS"
        )
    addressing = DeviceAddress(adr)
    instance = InstanceAddress()
    set_device_dtr0(dali, address)
    write_device_frame(
        dali,
        addressing.byte,
        instance.byte,
        DeviceConfigureCommandOpcode.SET_SHORT_ADDRESS,
        True,
    )


@click.command(name="add", help="Add to group.")
@click.pass_obj
@device_address_option
@click.argument("group", type=click.INT)
def add(dali: DaliInterface, adr: str, group: int):
    if 0 <= group < DaliMax.DEVICE_GROUP:
        address = DeviceAddress(adr)
        instance = InstanceAddress()
        if address.isvalid():
            if 0 <= group < 8:
                set_device_dtr2_dtr1(dali, 0, 1 << group)
                write_device_frame(
                    dali,
                    address.byte,
                    instance.byte,
                    DeviceConfigureCommandOpcode.ADD_TO_DEVICE_GROUPS_0_15,
                    True,
                )
            elif 8 <= group < 16:
                set_device_dtr2_dtr1(dali, 1 << (group - 8), 0)
                write_device_frame(
                    dali,
                    address.byte,
                    instance.byte,
                    DeviceConfigureCommandOpcode.ADD_TO_DEVICE_GROUPS_0_15,
                    True,
                )
            elif 16 <= group < 24:
                set_device_dtr2_dtr1(dali, 0, 1 << (group - 16))
                write_device_frame(
                    dali,
                    address.byte,
                    instance.byte,
                    DeviceConfigureCommandOpcode.ADD_TO_DEVICE_GROUPS_16_31,
                    True,
                )
            else:
                set_device_dtr2_dtr1(dali, 1 << (group - 24), 0)
                write_device_frame(
                    dali,
                    address.byte,
                    instance.byte,
                    DeviceConfigureCommandOpcode.ADD_TO_DEVICE_GROUPS_16_31,
                    True,
                )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.DEVICE_GROUP-1}", param_hint="GROUP"
        )


@click.command(name="ungroup", help="Remove from group.")
@click.pass_obj
@device_address_option
@click.argument("group", type=click.INT)
def ungroup(dali: DaliInterface, adr: str, group: int):
    if 0 <= group < DaliMax.DEVICE_GROUP:
        address = DeviceAddress(adr)
        instance = InstanceAddress()
        if address.isvalid():
            if 0 <= group < 8:
                set_device_dtr2_dtr1(dali, 0, 1 << group)
                write_device_frame(
                    dali,
                    address.byte,
                    instance.byte,
                    DeviceConfigureCommandOpcode.REMOVE_FROM_DEVICE_GROUPS_0_15,
                    True,
                )
            elif 8 <= group < 16:
                set_device_dtr2_dtr1(dali, 1 << (group - 8), 0)
                write_device_frame(
                    dali,
                    address.byte,
                    instance.byte,
                    DeviceConfigureCommandOpcode.REMOVE_FROM_DEVICE_GROUPS_0_15,
                    True,
                )
            elif 16 <= group < 24:
                set_device_dtr2_dtr1(dali, 0, 1 << (group - 16))
                write_device_frame(
                    dali,
                    address.byte,
                    instance.byte,
                    DeviceConfigureCommandOpcode.REMOVE_FROM_DEVICE_GROUPS_16_31,
                    True,
                )
            else:
                set_device_dtr2_dtr1(dali, 1 << (group - 24), 0)
                write_device_frame(
                    dali,
                    address.byte,
                    instance.byte,
                    DeviceConfigureCommandOpcode.REMOVE_FROM_DEVICE_GROUPS_16_31,
                    True,
                )
    else:
        raise click.BadParameter(
            f"needs to be between 0 and {DaliMax.DEVICE_GROUP-1}", param_hint="GROUP"
        )
