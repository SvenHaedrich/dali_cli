import click
import dali
import logging
from queue import Empty
from .address import DaliAddressByte

logger = logging.getLogger(__name__)


def gear_send_forward_frame(adr, opcode, send_twice=False):
    logging.debug("gear_send_forward_frame")
    address = DaliAddressByte()
    if address.arg(adr):
        command = address.byte << 8 | opcode
        dali.connection.transmit(length=16, data=command, send_twice=send_twice)
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")


def gear_query_value(adr, opcode):
    logging.debug("gear_query_value")
    dali.connection.start_receive()
    address = DaliAddressByte()
    if address.arg(adr):
        command = address.byte << 8 | opcode
        dali.connection.transmit(length=16, data=command)
        while True:
            try:
                dali.connection.get_next(dali.timeout_sec)
            except Empty:
                logging.debug("no frame received")
                dali.connection.close()
                return None
            if dali.connection.data == dali.connection.last_transmit:
                logging.debug("received query command")
                continue
            if dali.connection.length == 8:
                logging.debug("received backward frame")
                break
        dali.connection.close()
        return dali.connection.data
    else:
        raise click.BadOptionUsage("adr", "invalid address option.")
    dali.connection.close()
    return None


def gear_query_and_display_reply(adr, opcode):
    dali.connection.start_receive()
    address = DaliAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    dali.connection.transmit(length=16, data=command)
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
        command = 0xA3 << 8 | value
        dali.connection.transmit(length=16, data=command)
        while True:
            dali.connection.get_next(dali.timeout_sec)
            if dali.connection.data == dali.connection.last_transmit:
                return
    else:
        raise click.BadParameter(
            "needs to be between 0 and 255.", param_hint=parameter_hint
        )
