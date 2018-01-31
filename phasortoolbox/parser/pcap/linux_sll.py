# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from enum import Enum
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from .ipv4_packet import Ipv4Packet
from .ipv6_packet import Ipv6Packet
class LinuxSll(KaitaiStruct):

    class EtherTypeEnum(Enum):
        ipv4 = 2048
        x_75_internet = 2049
        nbs_internet = 2050
        ecma_internet = 2051
        chaosnet = 2052
        x_25_level_3 = 2053
        arp = 2054
        ipv6 = 34525
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.packet_type = self._io.read_u2be()
        self.arphrd_type = self._io.read_u2be()
        self.link_layer_address_length = self._io.read_u2be()
        self.src_addr = self._io.read_bytes(8)
        self.ether_type = self._root.EtherTypeEnum(self._io.read_u2be())
        _on = self.ether_type
        if _on == self._root.EtherTypeEnum.ipv4:
            self._raw_body = self._io.read_bytes_full()
            io = KaitaiStream(BytesIO(self._raw_body))
            self.body = Ipv4Packet(io)
        elif _on == self._root.EtherTypeEnum.ipv6:
            self._raw_body = self._io.read_bytes_full()
            io = KaitaiStream(BytesIO(self._raw_body))
            self.body = Ipv6Packet(io)
        else:
            self.body = self._io.read_bytes_full()
