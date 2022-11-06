class DALIAddressByte:

    DAPC = 'DAPC'
    SHORT = 'SHORT'
    GROUP = 'GROUP'
    BROADCAST = 'BROADCAST'
    UNADDRESSED = 'UNADDRESSED'
    SPECIAL = 'SPECIAL'
    RESERVED = 'RESERVED'
    INVALID = 'INVALID'

    def __init__(self, dapc=False):
        if dapc:
            self.byte = 0x00
        else:
            self.byte = 0x01
        self.mode = self.INVALID

    def short(self, address=0):
        if address in range(0x40):
            self.byte &= 0x01
            self.byte |= address << 1
            self.mode = self.SHORT

    def group(self, group=0):
        if group in range(0x10):
            self.byte &= 0x01
            self.byte |= group << 1
            self.byte |= 0x80
            self.mode = self.GROUP

    def broadcast(self):
        self.byte &= 0x01
        self.byte |= 0xFE
        self.mode = self.BROADCAST

    def unaddressed(self):
        self.byte &= 0x01
        self.byte |= 0xFC
        self.mode = self.UNADDRESSED

    def special(self, code=0):
        self.byte &= 0x01
        if code in range(0xA0,0xCC):
            self.byte |= code
            self.mode = self.SPECIAL

    def reserved(self, code=0):
        self.byte &= 0x01
        if code in range(0xCC,0xFC):
            self.byte |= code
            self.mode = self.RESERVED

    def arg(self, text=''):
        text = text.upper()
        if text == 'BC':
            self.broadcast()
            return
        if text == 'BCU':
            self.unaddressed()
            return
        if text[0] == 'A':
            self.short(int(text[1:2]))
            return
        if text[0] == 'G':
            self.group(int(text[1:2]))
            return

    def __str__(self):
        if self.mode == self.SHORT:
            short_address = (self.byte >> 1) & 0x3F
            return F'A{short_address:02}'
        elif self.mode == self.GROUP:
            group_address = (self.byte >> 1) & 0xF
            return F'G{group_address:02}'
        else:
            return self.mode
