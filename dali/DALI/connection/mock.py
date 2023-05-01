import logging

logger = logging.getLogger(__name__)


class DaliMock:
    def __init__(self):
        logger.debug("initialize mock interface")
        self.last_frame = None

    @staticmethod
    def convert_frame_to_serial_command(frame):
        if frame.send_twice:
            return f"T{frame.priority} {frame.length:X} {frame.data:X}"
        else:
            return f"S{frame.priority} {frame.length:X} {frame.data:X}"

    def start_read(self):
        logger.debug("start read")

    def read_raw_frame(self, timeout=None):
        return self.last_frame

    def write(self, frame):
        logger.debug("write frame")
        print(self.convert_frame_to_serial_command(frame))
        self.last_frame = frame

    def close(self):
        logger.debug("close mock interface")
