# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import array
import struct
import zlib
from enum import Enum
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Command(KaitaiStruct):

    class CommandCode(Enum):
        turn_off_transmission_of_data_frames = 1
        turn_on_transmission_of_data_frames = 2
        send_hdr_frame = 3
        send_cfg_1_frame = 4
        send_cfg_2_frame = 5
        send_cfg_3_frame = 6
        extended_frame = 8
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.cmd = self._root.CommandCode(self._io.read_u2be())
        self.ext = self._io.read_bytes_full()


