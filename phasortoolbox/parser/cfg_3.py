# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import array
import struct
import zlib
from enum import Enum
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Cfg3(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.cont_idx = self._io.read_u2be()
        self.time_base = self._root.TimeBase(self._io, self, self._root)
        self.num_pmu = self._io.read_u2be()
        self.station = [None] * (self.num_pmu)
        for i in range(self.num_pmu):
            self.station[i] = self._root.Cfg3Station(self._io, self, self._root)

        self.data_rate = self._io.read_s2be()

    class TimeBase(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.flags = self._io.read_bits_int(8)
            self.time_base = self._io.read_bits_int(24)


    class Cfg3Station(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.stn = self._root.Cfg3Station.Name(self._io, self, self._root)
            self.idcode = self._io.read_u2be()
            self.g_pmu_id = self._io.read_bytes(16)
            self.format = self._root.Cfg3Station.Format(self._io, self, self._root)
            self.phnmr = self._io.read_u2be()
            self.annmr = self._io.read_u2be()
            self.dgnmr = self._io.read_u2be()
            self.chnam = self._root.Cfg3Station.Chnam(self._io, self, self._root)
            self.phscale = [None] * (self.phnmr)
            for i in range(self.phnmr):
                self.phscale[i] = self._root.Cfg3Station.Phscale(self._io, self, self._root)

            self.anscale = [None] * (self.annmr)
            for i in range(self.annmr):
                self.anscale[i] = self._root.Cfg3Station.Anscale(self._io, self, self._root)

            self.digunit = [None] * (self.dgnmr)
            for i in range(self.dgnmr):
                self.digunit[i] = self._root.Cfg3Station.Digunit(self._io, self, self._root)

            self.pmu_lat = self._io.read_f4be()
            self.pmu_lon = self._io.read_f4be()
            self.pmu_elev = self._io.read_f4be()
            self.svc_class = (self._io.read_bytes(1)).decode(u"UTF-8")
            self.window = self._io.read_u4be()
            self.grp_dly = self._io.read_u4be()
            self.fnom = self._root.Cfg3Station.Fnom(self._io, self, self._root)
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
                self.freq_data_type = self._root.Cfg3Station.Format.IntFloat(self._io.read_bits_int(1))
                self.analogs_data_type = self._root.Cfg3Station.Format.IntFloat(self._io.read_bits_int(1))
                self.phasors_data_type = self._root.Cfg3Station.Format.IntFloat(self._io.read_bits_int(1))
                self.rectangular_or_polar = self._root.Cfg3Station.Format.RectangularPolar(self._io.read_bits_int(1))


        class Name(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.len = self._io.read_u1()
                self.name = (self._io.read_bytes(self.len)).decode(u"UTF-8")


        class Chnam(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.phasor_names = [None] * (self._parent.phnmr)
                for i in range(self._parent.phnmr):
                    self.phasor_names[i] = self._root.Cfg3Station.Name(self._io, self, self._root)

                self.analog_names = [None] * (self._parent.annmr)
                for i in range(self._parent.annmr):
                    self.analog_names[i] = self._root.Cfg3Station.Name(self._io, self, self._root)

                self.digital_status_labels = [None] * ((self._parent.dgnmr * 16))
                for i in range((self._parent.dgnmr * 16)):
                    self.digital_status_labels[i] = self._root.Cfg3Station.Name(self._io, self, self._root)



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


        class Anscale(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.magnitude_scaling = self._io.read_f4be()
                self.offset = self._io.read_f4be()


        class Phscale(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.modification_flags = self._root.Cfg3Station.Phscale.ModificationFlags(self._io, self, self._root)
                self.phasor_type_indication = self._root.Cfg3Station.Phscale.PhasorTypeIndication(self._io, self, self._root)
                self.user_designation = self._io.read_bytes(1)
                self.scale_factor = self._io.read_f4be()
                self.phasor_angle_adjustment = self._io.read_f4be()

            class ModificationFlags(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.modification_applied = self._io.read_bits_int(1) != 0
                    self.reserved = self._io.read_bits_int(4)
                    self.pseudo_phasor_value = self._io.read_bits_int(1) != 0
                    self.phasor_phase_adjusted_for_rotation = self._io.read_bits_int(1) != 0
                    self.phasor_phase_adjusted_for_calibration = self._io.read_bits_int(1) != 0
                    self.phasor_magnitude_adjusted_for_calibration = self._io.read_bits_int(1) != 0
                    self.filtered_without_changing_sampling = self._io.read_bits_int(1) != 0
                    self.down_sampled_with_nonfir_filter = self._io.read_bits_int(1) != 0
                    self.down_sampled_with_fir_filter = self._io.read_bits_int(1) != 0
                    self.down_sampled_by_reselection = self._io.read_bits_int(1) != 0
                    self.up_sampled_with_extrapolation = self._io.read_bits_int(1) != 0
                    self.up_sampled_with_interpolation = self._io.read_bits_int(1) != 0
                    self.reserved = self._io.read_bits_int(1) != 0


            class PhasorTypeIndication(KaitaiStruct):

                class VoltageOrCurrentEnum(Enum):
                    voltage = 0
                    current = 1

                class PhasorComponentEnum(Enum):
                    zero_sequence = 0
                    positive_sequence = 1
                    negative_sequence = 2
                    reserved_011 = 3
                    phase_a = 4
                    phase_b = 5
                    phase_c = 6
                    reserved_111 = 7
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.reserved = self._io.read_bits_int(4)
                    self.voltage_or_current = self._root.Cfg3Station.Phscale.PhasorTypeIndication.VoltageOrCurrentEnum(self._io.read_bits_int(1))
                    self.phasor_component = self._root.Cfg3Station.Phscale.PhasorTypeIndication.PhasorComponentEnum(self._io.read_bits_int(3))





