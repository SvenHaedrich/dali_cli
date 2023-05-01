import serial
import logging
import queue
import threading
import time

logger = logging.getLogger(__name__)


class DaliSerial:
    DEFAULT_BAUDRATE = 115200
    QUEUE_MAXSIZE = 40

    def __init__(self, port, baudrate=DEFAULT_BAUDRATE, transparent=False):
        logger.debug("open serial port")
        self.queue = queue.Queue(maxsize=self.QUEUE_MAXSIZE)
        self.port = serial.Serial(port=port, baudrate=baudrate, timeout=0.2)
        self.transparent = transparent
        self.length = None
        self.data = None
        self.type = None
        self.last_transmit = None

    def parse(self, line):
        try:
            start = line.find(ord("{")) + 1
            end = line.find(ord("}"))
            payload = line[start:end]
            timestamp = int(payload[0:8], 16) / 1000.0
            type = int(payload[8])
            length = int(payload[9:11], 16)
            data = int(payload[12:20], 16)
            return (timestamp, type, length, data)
        except ValueError:
            return None

    def read_worker_thread(self):
        logger.debug("read_worker_thread started")
        while self.keep_running:
            line = self.port.readline()
            if self.transparent:
                print(line.decode("utf-8"), end="")
            if len(line) > 0:
                logger.debug(f"received line <{line}> from serial")
                self.queue.put(self.parse(line))
        logger.debug("read_worker_thread terminated")

    def start_receive(self):
        logger.debug("start receive")
        self.keep_running = True
        self.thread = threading.Thread(target=self.read_worker_thread, args=())
        self.thread.daemon = True
        self.thread.start()

    def get_next(self, timeout=None):
        logger.debug("get next")
        result = self.queue.get(block=True, timeout=timeout)
        self.timestamp = result[0]
        self.type = result[1]
        self.length = result[2]
        self.data = result[3]
        return

    def transmit(self, length=0, data=0, priority=1, send_twice=False):
        logger.debug("transmit")
        if send_twice:
            self.port.write(f"T{priority} {length:X} {data:X}\r".encode("utf-8"))
        else:
            self.port.write(f"S{priority} {length:X} {data:X}\r".encode("utf-8"))
        self.last_transmit = data

    def close(self):
        logger.debug("close connection")
        self.keep_running = False
        while self.thread.is_alive():
            time.sleep(0.001)
        logger.debug("connection closed, thread terminated")
