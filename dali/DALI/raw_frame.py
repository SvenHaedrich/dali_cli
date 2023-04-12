import logging

logger = logging.getLogger(__name__)

class Raw_Frame:
    COMMAND = '-'
    ERROR = '*'
    INVALID = ' '

    def reset_self(self):
        self.timestamp = 0
        self.type = self.INVALID
        self.length = 0
        self.data = 0
        self.twice = False


    def from_line(self, line):
        if self.echo:
            print(line.decode('utf-8'), end='')
        try:
            start = line.find(ord('{'))+1
            end = line.find(ord('}'))
            payload = line[start:end]
            self.timestamp = int(payload[0:8], 16) / 1000.0
            self.type = chr(payload[8])
            self.length = int(payload[9:11], 16)
            self.data = int(payload[12:20], 16)
        except ValueError:
            self.reset_self()
            self.type = self.INVALID
        logger.debug("Raw frame, length {} data 0x{:08X}".format(self.length, self.data))


    def __init__(self, length=0, data=0, send_twice=False, echo=False):
        self.echo = echo
        self.reset_self()
        if (length-1) in range(0x20):
            self.length = length
            self.data = data
            self.send_twice = send_twice
