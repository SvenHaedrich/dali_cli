import click
import dali
import logging
from queue import Empty
from .address import DaliAddressByte
from .opcode import SpecialCommandOpcode
from ..connection.frame import DaliFrame


logger = logging.getLogger(__name__)


def gear_send_forward_frame(adr, opcode, send_twice=False):
    logging.debug("gear_send_forward_frame")
    address = DaliAddressByte()
    if address.arg(adr):
        command = address.byte << 8 | opcode
        dali.connection.transmit(
            DaliFrame(length=16, data=command, send_twice=send_twice)
        )
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")


def gear_query_value(adr, opcode):
    logging.debug("gear_query_value")
    address = DaliAddressByte()
    if address.arg(adr):
        command = address.byte << 8 | opcode
        dali.connection.transmit(DaliFrame(length=16, data=command))
        while True:
            try:
                dali.connection.get_next(dali.timeout_sec)
            except Empty:
                logging.debug("get_next timed out")
                return None
            if dali.connection.length == 8:
                logging.debug("received backward frame")
                break
            if dali.connection.type == DaliError.TIMEOUT:
                logging.debug("received no answer")
                return None
            if dali.connection.data == dali.connection.last_transmit:
                logging.debug("loopback of query command")
                continue
        return dali.connection.data
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")
    return None


def gear_query_and_display_reply(adr, opcode):
    dali.connection.start_receive()
    address = DaliAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    dali.connection.transmit(DaliFrame(length=16, data=command))
    answer = False
    try:
        while not answer:
            dali.connection.get_next(dali.timeout_sec)
            if dali.connection.data == dali.connection.last_transmit:
                continue
            if dali.connection.length == 8:
                answer = True
                click.echo(
                    f"0x{dali.connection.data:02X} = "
                    f"{dali.connection.data} = "
                    f"{dali.connection.data:08b}b"
                )
    except Empty:
        if not answer:
            click.echo("timeout - NO")
    dali.connection.close()


def set_dtr0(value, parameter_hint="UNKNOWN"):
    if value in range(dali.MAX_VALUE):
        command = SpecialCommandOpcode.DTR0 << 8 | value
        dali.connection.transmit(DaliFrame(length=16, data=command), block=True)
    else:
        raise click.BadParameter(
            "needs to be between 0 and 255.", param_hint=parameter_hint
        )


def set_dtr1(value, parameter_hint="UNKNOWN"):
    if value in range(dali.MAX_VALUE):
        command = SpecialCommandOpcode.DTR1 << 8 | value
        dali.connection.transmit(DaliFrame(length=16, data=command), block=True)
    else:
        raise click.BadParameter(
            "needs to be between 0 and 255.", param_hint=parameter_hint
        )


def write_gear_frame(address_byte, opcode_byte=0, send_twice=False):
    command = address_byte << 8 | opcode_byte
    dali.connection.transmit(DaliFrame(length=16, data=command, send_twice=send_twice))
    return


def write_frame_and_show_answer(address_byte, opcode_byte=0):
    dali.connection.start_receive()
    write_gear_frame(address_byte, opcode_byte)
    answer = False
    try:
        while not answer:
            dali.connection.get_next(dali.timeout_sec)
            if dali.connection.data == dali.connection.last_transmit:
                continue
            if dali.connection.length == 8:
                answer = True
                click.echo(
                    f"{dali.connection.data} ="
                    f"0x{dali.connection.data:02X} ="
                    f"{dali.connectopm.data:08b}b"
                )
    except Empty:
        if not answer:
            click.echo("timeout - NO")
