# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import array
import struct
import zlib
from enum import Enum
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from cfg_2_station import Cfg2Station
class Cfg2(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.time_base = self._root.TimeBase(self._io, self, self._root)
        self.num_pmu = self._io.read_u2be()
        self.station = [None] * (self.num_pmu)
        for i in range(self.num_pmu):
            self.station[i] = Cfg2Station(self._io)

        self.data_rate = self._io.read_s2be()

    class TimeBase(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.flags = self._io.read_bytes(1)
            self.time_base = self._io.read_bytes(3)



