from queue import Empty
import sys
import logging
import time

from DALI.forward_frame_16bit import ForwardFrame16Bit
from DALI.address_byte import DALIAddressByte
from DALI.raw_frame import Raw_Frame

import dali_serial
import dali_lunatone
import click


class Session:
    def __init__(self,connection):
        self.connection = connection

pass_session = click.make_pass_decorator(Session)

@click.group(name='dali')
@click.version_option('0.0.2')
@click.option(
    '--serial-port', 
    envvar='DALI_SERIAL_PORT',
    type=click.Path(),
    help='Serial port used for DALI communication.',
)
@click.option(
    '--lunatone',
    help='Use a Lunatone USB connector for DALI communication.',
    envvar='DALI_LUNATONE',
    is_flag=True,
)
@click.option(
    '--debug',
    is_flag=True,
    help='Enable debug logging.'
)
@click.pass_context
def cli(ctx,serial_port,lunatone,debug):
    """
    Command line interface for DALI systems.
    SevenLabs 2022
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    dali_connection = None
    if serial_port and not lunatone:
        dali_connection = dali_serial.DALI_Serial(port=serial_port,transparent=True)

    if lunatone and not serial_port:
        dali_connection = dali_lunatone.DALI_Usb()

    if dali_connection == None:
        click.echo("Illegal DALI source settings. Exit now.")
        sys.exit(2)

    ctx.obj = Session(dali_connection)

def simple_level_command(session, adr, mnemonic):
    address = DALIAddressByte()
    address.arg(adr)
    opcode  = ForwardFrame16Bit.opcode(mnemonic)
    command = address.byte << 8 | opcode
    frame = Raw_Frame(length=16, data=command)
    session.connection.write(frame)

@cli.command(name='off', help='Lights off.')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def off(session, adr):
    simple_level_command(session, adr, 'off')

@cli.command(name='up', help='Dim up.')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def min(session, adr):
    simple_level_command(session, adr, 'up')

@cli.command(name='down', help='Dim down.')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def min(session, adr):
    simple_level_command(session, adr, 'down')

@cli.command(name='max', help='Recall maximum.')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def max(session, adr):
    simple_level_command(session, adr, 'recall max level')

@cli.command(name='min', help='Recall minimum.')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def min(session, adr):
    simple_level_command(session, adr, 'recall min level')

@cli.command(name='dapc', help='Direct arc power control (dim level).')
@click.argument('level', type=click.INT)
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def dapc(session, adr, level):
    if level in range(0x100):
        address = DALIAddressByte(dapc=True)
        address.arg(adr)
        command = address.byte << 8 | level
        frame = Raw_Frame(length=16, data=command)
        session.connection.write(frame)

@cli.command(name='goto', help='Go to scene.')
@click.argument('scene', type=click.INT)
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def dapc(session, adr, scene):
    address = DALIAddressByte()
    address.arg(adr)
    opcode = ForwardFrame16Bit.opcode(F'GO TO SCENE {scene}')
    command = address.byte << 8 | opcode
    frame = Raw_Frame(length=16, data=command)
    session.connection.write(frame)

def gear_query_value(session, adr, opcode):
    session.connection.start_read()
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    session.connection.write(cmd_frame) 
    try:
        while True:
            frame = session.connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                session.connection.close()
                return frame.data
    except Empty:
        session.connection.close()
        return None

def gear_query_and_display_reply(session, adr, opcode):
    session.connection.start_read()
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    session.connection.write(cmd_frame) 
    answer = False
    try:
        while not answer:
            frame = session.connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                answer = True
                click.echo(F'{frame.data} = 0x{frame.data:02X} = {frame.data:08b}b')
    except Empty:
        if not answer:
            click.echo('timeout - NO')
    session.connection.close()

def gear_query_multiple(session, adr, opcode):
    address = DALIAddressByte()
    address.arg(adr)
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    session.connection.write(cmd_frame) 
    try:
        while True:
            frame = session.connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame.length == 8:
                return frame.data
    except Empty:
        return None

@click.group(name='gear', help='More control gear commands.')
def gear():
    pass

def gear_summary_item(session, adr, caption, command_mnemonic):
    result = gear_query_multiple(session, adr, ForwardFrame16Bit.opcode(command_mnemonic))
    if not result == None:
        click.echo(F'{caption:.<20}: {result} = 0x{result:02X} = {result:08b}b')
    else:
        click.echo(F'{caption:.<20}: NO - timeout')

@gear.command(name='summary', help='Show status summary.')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_summary(session, adr):
    session.connection.start_read()
    gear_summary_item(session,adr,'Status','QUERY STATUS')
    gear_summary_item(session,adr,'Operation mode','QUERY OPERATING MODE')
    gear_summary_item(session,adr,'Version','QUERY VERSION NUMBER')
    gear_summary_item(session,adr,'Actual level','QUERY ACTUAL LEVEL')
    gear_summary_item(session,adr,'Power on level','QUERY POWER ON LEVEL')
    gear_summary_item(session,adr,'System failure level','QUERY SYSTEM FAILURE LEVEL')
    gear_summary_item(session,adr,'Physical minimum','QUERY PHYSICAL MINIMUM')
    gear_summary_item(session,adr,'Minimum level','QUERY MIN LEVEL')
    gear_summary_item(session,adr,'Maximum level','QUERY MAX LEVEL')
    gear_summary_item(session,adr,'Device type','QUERY DEVICE TYPE')
    gear_summary_item(session,adr,'DTR0','QUERY CONTENT DTR0')
    gear_summary_item(session,adr,'DTR1','QUERY CONTENT DTR1')
    gear_summary_item(session,adr,'DTR2','QUERY CONTENT DTR2')
    random_h = gear_query_multiple(session, adr, ForwardFrame16Bit.opcode('QUERY RANDOM ADDRESS (H)'))
    random_m = gear_query_multiple(session, adr, ForwardFrame16Bit.opcode('QUERY RANDOM ADDRESS (M)'))
    random_l = gear_query_multiple(session, adr, ForwardFrame16Bit.opcode('QUERY RANDOM ADDRESS (L)'))
    random_address = random_h << 16 | random_m << 8 | random_l
    click.echo(F'Random address .....: {random_address} = 0x{random_address:06X} = {random_address:024b}b')
    session.connection.close()


@gear.command(name='list', help='List available short addresses.')
@pass_session
def gear_list(session):
    session.connection.start_read()
    opcode = 0x91
    address = DALIAddressByte()
    address.broadcast()
    command = address.byte << 8 | opcode
    cmd_frame = Raw_Frame(length=16, data=command)
    session.connection.write(cmd_frame) 
    answer = False
    try:
        while not answer:
            frame = session.connection.read_raw_frame(0.15)
            if frame.data == cmd_frame.data:
                continue
            if frame:
                answer = True
    except Empty:
        pass
    if answer:
        click.echo('Found control gears:')    
        for short_address in range (0x40):
            address.short(short_address)
            command = address.byte << 8 | opcode
            frame = Raw_Frame(length=16, data=command)
            session.connection.write(frame) 
            answer = False
            try:
                while not answer:
                    frame = session.connection.read_raw_frame(0.15)
                    if frame.data == cmd_frame.data:
                        continue
                    if frame.length == 8 and frame.data == 0xFF:
                        click.echo(F'A{short_address:02}')
            except Empty:
                pass
    session.connection.close()

@gear.command(name='set', help='Set control gear.')
def gear_set():
    pass

@click.group(name='query', help='Query control gear.')
def gear_query():
    pass

@gear_query.command(name='status', help='gear status byte')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    result = gear_query_value(session, adr, ForwardFrame16Bit.opcode('QUERY STATUS'))
    if not result == None:
        click.echo(F'Status: {result} = 0x{result:02X} = {result:08b}b')
        click.echo('Bit description')
        click.echo(F' {(result >> 0 & 0x01)} : controlGearFailure')
        click.echo(F' {(result >> 1 & 0x01)} : lampFailure')
        click.echo(F' {(result >> 2 & 0x01)} : lampOn')
        click.echo(F' {(result >> 3 & 0x01)} : limitError')
        click.echo(F' {(result >> 4 & 0x01)} : fadeRunning')
        click.echo(F' {(result >> 5 & 0x01)} : resetState')
        click.echo(F' {(result >> 6 & 0x01)} : shortAddress is MASK')
        click.echo(F' {(result >> 7 & 0x01)} : powerCycleSeen')
    else:
        click.echo('Status: NO - timeout')

@gear_query.command(name='present', help='control gear present')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_present(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY CONTROL GEAR PRESENT'))

@gear_query.command(name='lamp_failure', help='lamp failure')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY LAMP FAILURE'))

@gear_query.command(name='power', help='gear lamp power on')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY LAMP POWER ON'))

@gear_query.command(name='limit', help='limit error')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY LIMIT ERROR'))

@gear_query.command(name='reset', help='reset state')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY RESET STATE'))

@gear_query.command(name='short', help='missing short address')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY MISSING SHORT ADDRESS'))

@gear_query.command(name='version', help='version number')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    result = gear_query_value(session, adr, ForwardFrame16Bit.opcode('QUERY VERSION NUMBER'))
    if not result == None:
        click.echo(F'Version: {result} = 0x{result:02X} = {result:08b}b')
        click.echo(F' equals: {(result>>2)}.{(result&0x3)}')
    else:
        click.echo('Status: NO - timeout')

@gear_query.command(name='dtr0', help='content DTR0')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY CONTEND DTR0'))

@gear_query.command(name='dt', help='device type')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY DEVICE TYPE'))

@gear_query.command(name='next', help='next device type')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY NEXT DEVICE TYPE'))

@gear_query.command(name='phm', help='physical minimum')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY PHYSICAL MINIMUM'))

@gear_query.command(name='power_cycle', help='power cycle seen')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY POWER FAILURE'))

@gear_query.command(name='dtr1', help='content DTR1')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY CONTENT DTR1'))

@gear_query.command(name='dtr2', help='content DTR2')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY CONTENT DTR2'))

@gear_query.command(name='op', help='operating mode')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY OPERATING MODE'))

@gear_query.command(name='light', help='light source type')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY LIGHT SOURCE TYPE'))

@gear_query.command(name='actual', help='actual level')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY ACTUAL LEVEL'))

@gear_query.command(name='max', help='maximum light level')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY MAX LEVEL'))

@gear_query.command(name='min', help='minimum light level')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY MIN LEVEL'))

@gear_query.command(name='on', help='power on light level')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY POWER ON LEVEL'))

@gear_query.command(name='fail', help='system failure light level')
@click.option('--adr', default='BC', help='Address, can be a short address (A0..A63) or group address (G0..G15).')
@pass_session
def gear_query_status(session, adr):
    gear_query_and_display_reply(session, adr, ForwardFrame16Bit.opcode('QUERY SYSTEM FAILURE LEVEL'))

@gear.command(name='dtr0')
def gear_dtr0():
    pass

@click.group(name='device', help='Control device commands.')
def device():
    pass

@device.command(name='list')
def device_list():
    click.echo('device list')

cli.add_command(gear)
gear.add_command(gear_query)
cli.add_command(device)
