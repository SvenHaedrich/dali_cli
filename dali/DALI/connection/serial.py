import serial
import logging
import queue
import threading
import time
from ..frame import DaliRxFrame

logger = logging.getLogger(__name__)


class DaliSerial:
    DEFAULT_BAUDRATE = 115200
    QUEUE_MAXSIZE = 40

    def __init__(self, port, baudrate=DEFAULT_BAUDRATE, transparent=False):
        logger.debug("open serial port")
        self.queue = queue.Queue(maxsize=self.QUEUE_MAXSIZE)
        self.port = serial.Serial(port=port, baudrate=baudrate, timeout=0.2)
        self.transparent = transparent

    @staticmethod
    def line_to_frame(line):
        try:
            start = line.find(ord("{")) + 1
            end = line.find(ord("}"))
            payload = line[start:end]
            timestamp = int(payload[0:8], 16) / 1000.0
            type = int(payload[8])
            length = int(payload[9:11], 16)
            data = int(payload[12:20], 16)
            return DaliRxFrame(timestamp, type, length, data)
        except ValueError:
            return None

    def read_worker_thread(self):
        logger.debug("read_worker_thread started")
        while self.keep_running:
            logger.debug(f"keep_running {self.keep_running}")
            line = self.port.readline()
            if self.transparent:
                print(line.decode("utf-8"), end="")
            if len(line) > 0:
                logger.debug(f"received line <{line}> from serial")
                self.queue.put(self.line_to_frame(line))
        logger.debug("read_worker_thread terminated")

    def start_read(self):
        logger.debug("start read")
        self.keep_running = True
        self.thread = threading.Thread(target=self.read_worker_thread, args=())
        self.thread.daemon = True
        self.thread.start()

    def read_raw_frame(self, timeout=None):
        return self.queue.get(block=True, timeout=timeout)

    @staticmethod
    def convert_frame_to_serial_command(frame):
        if frame.send_twice:
            return f"T{frame.priority} {frame.length:X} {frame.data:X}\r".encode(
                "utf-8"
            )
        else:
            return f"S{frame.priority} {frame.length:X} {frame.data:X}\r".encode(
                "utf-8"
            )

    def write(self, frame):
        logger.debug("write frame")
        self.port.write(self.convert_frame_to_serial_command(frame))

    def close(self):
        logger.debug("close connection")
        self.keep_running = False
        while self.thread.is_alive():
            time.sleep(0.001)
        logger.debug("connection closed, thread terminated")
