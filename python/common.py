# This is modified from a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import array
import struct
import zlib
from enum import Enum
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO

if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from cfg_2 import Cfg2
from header import Header
from data import Data
from cfg_3 import Cfg3
from command import Command


class Common(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None, _mini_cfg=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._pkt_pos = self._io.pos()
        self._mini_cfg = _mini_cfg
        self.sync = self._root.SyncWord(self._io, self, self._root)
        self.framesize = self._io.read_u2be()
        self.idcode = self._io.read_u2be()
        self.soc = self._io.read_u4be()
        self.fracsec = self._root.Fracsec(self._io, self, self._root,
                                          self._mini_cfg.time_base if self._mini_cfg else None)
        _on = self.sync.frame_type.name
        if _on == 'data_frame':
            self._raw_data = self._io.read_bytes((self.framesize - 16))
            io = KaitaiStream(BytesIO(self._raw_data))
            self.data = Data(io, _mini_cfg = self._mini_cfg)
            #self.data = self._io.read_bytes((self.framesize - 16))#
            #self.data = Data(self._io, _mini_cfg = self._mini_cfg)
        elif _on == 'command_frame':
            self._raw_data = self._io.read_bytes((self.framesize - 16))
            io = KaitaiStream(BytesIO(self._raw_data))
            self.data = Command(io)
        elif _on == 'header_frame':
            self._raw_data = self._io.read_bytes((self.framesize - 16))
            io = KaitaiStream(BytesIO(self._raw_data))
            self.data = Header(io)
        elif _on == 'configuration_frame_2':
            self._raw_data = self._io.read_bytes((self.framesize - 16))
            io = KaitaiStream(BytesIO(self._raw_data))
            self.data = Cfg2(io)
        elif _on == 'configuration_frame_3':
            self._raw_data = self._io.read_bytes((self.framesize - 16))
            io = KaitaiStream(BytesIO(self._raw_data))
            self.data = Cfg3(io)
        elif _on == 'configuration_frame_1':
            self._raw_data = self._io.read_bytes((self.framesize - 16))
            io = KaitaiStream(BytesIO(self._raw_data))
            self.data = Cfg2(io)
        self.chk = self._io.read_u2be()

    class SyncWord(KaitaiStruct):

        class FrameTypeEnum(Enum):
            data_frame = 0
            header_frame = 1
            configuration_frame_1 = 2
            configuration_frame_2 = 3
            command_frame = 4
            configuration_frame_3 = 5

        class VersionNumberEnum(Enum):
            c_37_118_2005 = 1
            c_37_118_2_2011 = 2

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.magic = self._io.ensure_fixed_contents(struct.pack('1b', -86))
            self.reserved = self._io.read_bits_int(1) != 0
            self.frame_type = self._root.SyncWord.FrameTypeEnum(self._io.read_bits_int(3))
            self.version_number = self._root.SyncWord.VersionNumberEnum(self._io.read_bits_int(4))

    class Fracsec(KaitaiStruct):

        class LeapSecondDirectionEnum(Enum):
            add = 0
            delete = 1

        class MsgTq(Enum):
            normal_operation_clock_locked_to_utc_traceable_source = 0
            time_within_10_to_9_s_of_utc = 1
            time_within_10_to_8_s_of_utc = 2
            time_within_10_to_7_s_of_utc = 3
            time_within_10_to_6_s_of_utc = 4
            time_within_10_to_5_s_of_utc = 5
            time_within_10_to_4_s_of_utc = 6
            time_within_10_to_3_s_of_utc = 7
            time_within_10_to_2_s_of_utc = 8
            time_within_10_to_1_s_of_utc = 9
            time_within_1_s_of_utc = 10
            time_within_10_s_of_utc = 11
            fault_clock_failure_time_not_reliable = 15

        def __init__(self, _io, _parent=None, _root=None, _time_base=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._time_base = _time_base
            self.reserved = self._io.read_bits_int(1) != 0
            self.leap_second_direction = self._root.Fracsec.LeapSecondDirectionEnum(self._io.read_bits_int(1))
            self.leap_second_occurred = self._io.read_bits_int(1) != 0
            self.leap_second_pending = self._io.read_bits_int(1) != 0
            self.time_quailty = self._root.Fracsec.MsgTq(self._io.read_bits_int(4))
            self.raw_fraction_of_second = self._io.read_bits_int(24)

        @property
        def fraction_of_second(self):
            if hasattr(self, '_m_fraction_of_second'):
                return self._m_fraction_of_second if hasattr(self, '_m_fraction_of_second') else None

            if self._time_base:
                self._m_fraction_of_second = self.raw_fraction_of_second / self._time_base

            return self._m_fraction_of_second if hasattr(self, '_m_fraction_of_second') else None

    @property
    def chk_body(self):
        if hasattr(self, '_m_chk_body'):
            return self._m_chk_body if hasattr(self, '_m_chk_body') else None

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_chk_body = self._io.read_bytes((self.framesize - 2))
        self._io.seek(_pos)
        return self._m_chk_body if hasattr(self, '_m_chk_body') else None

    @property
    def pkt(self):
        if hasattr(self, '_m_pkt'):
            return self._m_pkt if hasattr(self, '_m_pkt') else None

        _pos = self._io.pos()
        self._io.seek(self._pkt_pos)
        self._m_pkt = self._io.read_bytes(self.framesize)
        self._io.seek(_pos)
        return self._m_pkt if hasattr(self, '_m_pkt') else None
