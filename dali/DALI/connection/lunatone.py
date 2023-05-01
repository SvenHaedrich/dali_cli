import errno
import logging
import queue
import struct
import threading
import time
import usb
from .. import frame

logger = logging.getLogger(__name__)


class DaliUsb:
    DALI_USB_VENDOR = 0x17B5
    DALI_USB_PRODUCT = 0x0020

    DALI_USB_DIRECTION_FROM_DALI = 0x11
    DALI_USB_DIRECTION_TO_DALI = 0x12
    DALI_USB_TYPE_NO = 0x01
    DALI_USB_TYPE_8BIT = 0x02
    DALI_USB_TYPE_16BIT = 0x03
    DALI_USB_TYPE_25BIT = 0x04
    DALI_USB_TYPE_24BIT = 0x06
    DALI_USB_TYPE_STATUS = 0x07
    DALI_USB_RECEIVE_MASK = 0x70

    def __init__(self, vendor=DALI_USB_VENDOR, product=DALI_USB_PRODUCT):
        # lookup devices by vendor and DALI_USB_PRODUCT
        self.interface = 0
        self.queue = queue.Queue(maxsize=40)
        self.keep_running = False
        self.message_counter = 1

        logger.debug("try to discover DALI interfaces")
        devices = [
            dev
            for dev in usb.core.find(find_all=True, idVendor=vendor, idProduct=product)
        ]

        # if not found
        if devices:
            logger.info(f"DALI interfaces found: {devices}")
        else:
            raise usb.core.USBError("DALI interface not found")

        # use first device from list
        self.device = devices[0]
        self.device.reset()

        # detach kernel driver if necessary
        if self.device.is_kernel_driver_active(self.interface) is True:
            self.device.detach_kernel_driver(self.interface)

        # set device configuration
        self.device.set_configuration()

        # claim interface
        usb.util.claim_interface(self.device, self.interface)

        # get active configuration
        cfg = self.device.get_active_configuration()
        intf = cfg[(0, 0)]

        # get read and write endpoints
        self.ep_write = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_OUT,
        )

        self.ep_read = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_IN,
        )

        if not self.ep_read or not self.ep_write:
            raise usb.core.USBError(
                f"could not determine read or write endpoint on {self.device}"
            )

        # read pending messages and disregard
        try:
            while True:
                self.ep_read.read(self.ep_read.wMaxPacketSize, timeout=10)
                logger.info("DALI interface - disregard pending messages")
        except Exception:
            pass

    def read_raw(self, timeout=None):
        return self.ep_read.read(self.ep_read.wMaxPacketSize, timeout=timeout)

    def write(self, frame):
        """Write data to DALI bus.
        cmd : tupel of bytes to send

        Data expected by DALI USB
        dr sn ?? ty ?? ec ad oc.. .. .. .. .. .. .. ..
        12 xx 00 03 00 00 ff 08 00 00 00 00 00 00 00 00

        dr: direction
            0x12 = USB side
        sn: sequence number
        ec: eCommand
        ad: address
        oc: opcode
        """
        dr = self.DALI_USB_DIRECTION_TO_DALI
        sn = self.message_counter
        self.message_counter = (self.message_counter + 1) & 0xFF
        if frame.length == 24:
            ec = (frame.data >> 16) & 0xFF
            ad = (frame.data >> 8) & 0xFF
            oc = frame.data & 0xFF
            ty = self.DALI_USB_TYPE_24BIT
        elif frame.length == 16:
            ec = 0x00
            ad = (frame.data >> 8) & 0xFF
            oc = frame.data & 0xFF
            ty = self.DALI_USB_TYPE_16BIT
        elif frame.length == 8:
            ec = 0x00
            ad = 0x00
            oc = frame.data & 0xFF
            ty = self.DALI_USB_TYPE_8BIT
        else:
            raise Exception(
                f"DALI commands must be 8,16,24 bit long but {frame} is {frame.length} bit long"
            )

        data = struct.pack("BBxBxBBB" + (64 - 8) * "x", dr, sn, ty, ec, ad, oc)

        logger.debug(
            f"DALI[OUT]: SN=0x{sn:02X} TY=0x{ty:02X} EC=0x{ec:02X} AD=0x{ad:02X} OC=0x{oc:02X}"
        )
        result = self.ep_write.write(data)
        if frame.send_twice:
            frame.send_twice = False
            self.read_raw(timeout=100)
            time.sleep(0.014)
            self.write(frame)
        return result

    def close(self):
        logger.debug("close connection")
        self.keep_running = False
        while self.thread.is_alive():
            time.sleep(0.001)
        usb.util.dispose_resources(self.device)

    def read_worker_thread(self):
        logger.debug("read_worker_thread started")
        raw = DALI.Raw_Frame()
        while self.keep_running:
            try:
                data = self.read_raw(timeout=100)
                """ raw data received from DALI USB:
                dr ty ?? ec ad cm st st sn .. .. .. .. .. .. ..
                11 73 00 00 ff 93 ff ff 00 00 00 00 00 00 00 00

                dr: [0]: direction
                    0x11 = DALI side
                    0x12 = USB side
                ty: [1]: type
                ec: [2]: ecommand
                ad: [3]: address
                cm: [4] command
                    also serves as response code for 72
                st: [5] status
                    internal status code, value unknown
                sn: [6] seqnum
                """
                if data:
                    logger.debug(
                        f"DALI[IN]: SN=0x{data[8]:02X} TY=0x{data[1]:02X} EC=0x{data[3]:02X} AD=0x{data[4]:02X} OC=0x{data[5]:02X}"
                    )
                    type = Dali_Rx_Frame.COMMAND
                    if data[1] == (
                        self.DALI_USB_RECEIVE_MASK + self.DALI_USB_TYPE_8BIT
                    ):
                        length = 8
                        payload = data[5]
                    elif data[1] == (
                        self.DALI_USB_RECEIVE_MASK + self.DALI_USB_TYPE_16BIT
                    ):
                        length = 16
                        payload = data[5] + (data[4] << 8)
                    elif data[1] == (
                        self.DALI_USB_RECEIVE_MASK + self.DALI_USB_TYPE_24BIT
                    ):
                        length = 24
                        payload = data[5] + (data[4] << 8) + (data[3] << 16)
                    elif data[1] == (
                        self.DALI_USB_RECEIVE_MASK + self.DALI_USB_TYPE_STATUS
                    ):
                        type = Dali_Rx_Frame.ERROR
                        payload = 0
                        if data[5] == 0x04:
                            length = DALI.DALIError.RECOVER
                        elif data[5] == 0x03:
                            length = DALI.DALIError.FRAME
                        else:
                            length = DALI.DALIError.GENERAL
                    self.queue.put(Dali_Rx_Frame(time.time(), type, length, payload))

            except usb.USBError as e:
                if e.errno not in (errno.ETIMEDOUT, errno.ENODEV):
                    raise e
        logger.debug("read_worker_thread terminated")

    def start_read(self):
        logger.debug("start read")
        self.keep_running = True
        self.thread = threading.Thread(target=self.read_worker_thread, args=())
        self.thread.daemon = True
        self.thread.start()

    def read_raw_frame(self, timeout=None):
        return self.queue.get(block=True, timeout=timeout)
