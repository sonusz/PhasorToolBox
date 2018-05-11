# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import array
import struct
import zlib
from enum import Enum
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Cfg2(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.time_base = self._root.TimeBase(self._io, self, self._root)
        self.num_pmu = self._io.read_u2be()
        self.station = [None] * (self.num_pmu)
        for i in range(self.num_pmu):
            self.station[i] = self._root.Cfg2Station(self._io, self, self._root)

        self.data_rate = self._io.read_s2be()

    class TimeBase(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.flags = self._io.read_bits_int(8)
            self.time_base = self._io.read_bits_int(24)


    class Cfg2Station(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.stn = self._root.Cfg2Station.Name(self._io, self, self._root)
            self.idcode = self._io.read_u2be()
            self.format = self._root.Cfg2Station.Format(self._io, self, self._root)
            self.phnmr = self._io.read_u2be()
            self.annmr = self._io.read_u2be()
            self.dgnmr = self._io.read_u2be()
            self.chnam = self._root.Cfg2Station.Chnam(self._io, self, self._root)
            self.phunit = [None] * (self.phnmr)
            for i in range(self.phnmr):
                self.phunit[i] = self._root.Cfg2Station.Phunit(self._io, self, self._root)

            self.anunit = [None] * (self.annmr)
            for i in range(self.annmr):
                self.anunit[i] = self._root.Cfg2Station.Anunit(self._io, self, self._root)

            self.digunit = [None] * (self.dgnmr)
            for i in range(self.dgnmr):
                self.digunit[i] = self._root.Cfg2Station.Digunit(self._io, self, self._root)

            self.fnom = self._root.Cfg2Station.Fnom(self._io, self, self._root)
            self.cfgcnt = self._io.read_u2be()

        class Format(KaitaiStruct):

            class IntFloat(Enum):
                int = 0
                float = 1

            class RectangularPolar(Enum):
                rectangular = 0
                polar = 1
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.unused = self._io.read_bits_int(12)
                self.freq_data_type = self._root.Cfg2Station.Format.IntFloat(self._io.read_bits_int(1))
                self.analogs_data_type = self._root.Cfg2Station.Format.IntFloat(self._io.read_bits_int(1))
                self.phasors_data_type = self._root.Cfg2Station.Format.IntFloat(self._io.read_bits_int(1))
                self.rectangular_or_polar = self._root.Cfg2Station.Format.RectangularPolar(self._io.read_bits_int(1))


        class Name(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.name = (self._io.read_bytes(16)).decode(u"UTF-8")


        class Anunit(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.analog_input = self._io.read_u1()
                self.raw_conversion_factor = self._io.read_bits_int(24)

            @property
            def conversion_factor(self):
                if hasattr(self, '_m_conversion_factor'):
                    return self._m_conversion_factor if hasattr(self, '_m_conversion_factor') else None

                self._m_conversion_factor = (self.raw_conversion_factor if self.raw_conversion_factor <= 8388607 else self.raw_conversion_factorif - 16777215)
                return self._m_conversion_factor if hasattr(self, '_m_conversion_factor') else None


        class Chnam(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.phasor_names = [None] * (self._parent.phnmr)
                for i in range(self._parent.phnmr):
                    self.phasor_names[i] = self._root.Cfg2Station.Name(self._io, self, self._root)

                self.analog_names = [None] * (self._parent.annmr)
                for i in range(self._parent.annmr):
                    self.analog_names[i] = self._root.Cfg2Station.Name(self._io, self, self._root)

                self.digital_status_labels = [None] * ((self._parent.dgnmr * 16))
                for i in range((self._parent.dgnmr * 16)):
                    self.digital_status_labels[i] = self._root.Cfg2Station.Name(self._io, self, self._root)



        class Digunit(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.normal_status = "{0:016b}".format(self._io.read_bits_int(16))
                self.current_valid_inputs = "{0:016b}".format(self._io.read_bits_int(16))


        class Fnom(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.reserved = self._io.read_bits_int(15)
                self.raw_fundamental_frequency = self._io.read_bits_int(1) != 0

            @property
            def fundamental_frequency(self):
                if hasattr(self, '_m_fundamental_frequency'):
                    return self._m_fundamental_frequency if hasattr(self, '_m_fundamental_frequency') else None

                self._m_fundamental_frequency = (60 - (int(self.raw_fundamental_frequency) * 10))
                return self._m_fundamental_frequency if hasattr(self, '_m_fundamental_frequency') else None


        class Phunit(KaitaiStruct):

            class VoltageOrCurrentEnum(Enum):
                voltage = 0
                current = 1
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.voltage_or_current = self._root.Cfg2Station.Phunit.VoltageOrCurrentEnum(self._io.read_u1())
                self.raw_conversion_factor = self._io.read_bits_int(24)

            @property
            def conversion_factor(self):
                if hasattr(self, '_m_conversion_factor'):
                    return self._m_conversion_factor if hasattr(self, '_m_conversion_factor') else None

                self._m_conversion_factor = (self.raw_conversion_factor / 100000.0)
                return self._m_conversion_factor if hasattr(self, '_m_conversion_factor') else None




