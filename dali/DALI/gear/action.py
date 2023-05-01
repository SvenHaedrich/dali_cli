import click
import dali
import logging
from queue import Empty
from .address import DaliAddressByte
from ..frame import DaliTxFrame

logger = logging.getLogger(__name__)


def gear_send_forward_frame(adr, opcode, send_twice=False):
    logging.debug("gear_send_forward_frame")
    address = DaliAddressByte()
    if address.arg(adr):
        command = address.byte << 8 | opcode
        frame = DaliTxFrame(length=16, data=command, send_twice=send_twice)
        dali.connection.write(frame)
        return frame
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")


def gear_query_value(adr, opcode):
    logging.debug("gear_query_value")
    dali.connection.start_read()
    address = DaliAddressByte()
    if address.arg(adr):
        command = address.byte << 8 | opcode
        cmd_frame = DaliTxFrame(length=16, data=command)
        dali.connection.write(cmd_frame)
        while True:
            try:
                frame = dali.connection.read_raw_frame(dali.timeout_sec)
            except Empty:
                logging.debug("no frame received")
                break
            if frame.data == cmd_frame.data:
                logging.debug("received query command")
                continue
            if frame.length == 8:
                logging.debug("received backward frame")
                break
        return frame.data
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")


def gear_query_and_display_reply(adr, opcode):
    dali.connection.start_read()
    address = DaliAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = DaliTxFrame(length=16, data=command)
    dali.connection.write(cmd_frame)
    answer = False
    try:
        while not answer:
            frame = dali.connection.read_raw_frame(dali.timeout_sec)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                answer = True
                click.echo(f"0x{frame.data:02X} = {frame.data} = {frame.data:08b}b")
    except Empty:
        if not answer:
            click.echo("timeout - NO")


def set_dtr0(value, parameter_hint="UNKNOWN"):
    if value in range(dali.MAX_VALUE):
        dali.connection.start_read()
        command = 0xA3 << 8 | value
        command_frame = DaliTxFrame(length=16, data=command)
        dali.connection.write(command_frame)
        while True:
            readback = dali.connection.read_raw_frame(timeout=dali.timeout_sec)
            if command_frame.data == readback.data:
                return
    else:
        raise click.BadParameter(
            "needs to be between 0 and 255.", param_hint=parameter_hint
        )
