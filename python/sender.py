
class Client(object):
    def __init__(self, serverIP = None):

class Messenger(object):
    def __init__(self,):
        self.sync = self._root.SyncWord(self._io, self, self._root)
        self.framesize = self._io.read_u2be()
        self.idcode = self._io.read_u2be()
        self.soc = self._io.read_u4be()
        self.fracsec = self._root.Fracsec(self._io, self, self._root,
    def sync(self):

    def idcode(self):
        return '{:04x}'.format(self.ID)

    def soc_time(self):
        return '{:08x}'.format(int(time.time())) + '00' + '{:06x}'.format(int(time.time() % 1 * 16777215))


    def checksum(self, s):
        return '{:04x}'.format(crc16.crc16xmodem(s.decode('hex'), 0xffff))
