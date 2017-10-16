# This is modified from a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import array
import struct
import zlib
from enum import Enum

import cmath
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Data(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None, _mini_cfg = None): # Add  _mini_cfg
        """

        :param _io:
        :param _parent:
        :param _root:
        :param _mini_cfg:
        """
        self._mini_cfg = _mini_cfg
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.pmu_data = [None] * (self._mini_cfg.num_pmu)
        for i in range(self._mini_cfg.num_pmu):
            self.pmu_data[i] = self._root.PmuData(self._io, self, self._root, _station = self._mini_cfg.station[i])


    class PmuData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None, _station = None):
            self._station = _station
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.stat = self._root.PmuData.Stat(self._io, self, self._root)
            self.phasors = [None] * (self._station.phnmr)
            for i in range(self._station.phnmr):
                self.phasors[i] = self._root.PmuData.Phasors(self._io, self, self._root, self._station.phunit[i])

            self.freq = self._root.PmuData.Freq(self._io, self, self._root).freq.freq
            self.dfreq = self._root.PmuData.Dfreq(self._io, self, self._root)
            self.analog = [None] * (self._station.annmr)
            for i in range(self._station.annmr):
                self.analog[i] = self._root.PmuData.Analog(self._io, self, self._root, self._station.anunit[i])

            self.digital = [None] * (self._station.dgnmr)
            for i in range(self._station.dgnmr):
                self.digital[i] = self._io.read_bits_int(16)


        class Freq(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                _on = self._parent._station.format.freq_data_type
                if _on == 'int':
                    self.freq = self._root.PmuData.Freq.Int(self._io, self, self._root)
                elif _on == 'float':
                    self.freq = self._root.PmuData.Freq.Float(self._io, self, self._root)

            class Int(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.raw_freq = self._io.read_s2be()

                @property
                def freq(self):
                    if hasattr(self, '_m_freq'):
                        return self._m_freq if hasattr(self, '_m_freq') else None

                    self._m_freq = ((self.raw_freq / 1000.0) + self._parent._parent._station.fnom.fundamental_frequency)
                    return self._m_freq if hasattr(self, '_m_freq') else None


            class Float(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.raw_freq = self._io.read_f4be()

                @property
                def freq(self):
                    if hasattr(self, '_m_freq'):
                        return self._m_freq if hasattr(self, '_m_freq') else None

                    self._m_freq = self.raw_freq
                    return self._m_freq if hasattr(self, '_m_freq') else None



        class Stat(KaitaiStruct):

            class PmuTimeQualityEnum(Enum):
                not_used = 0
                estimated_maximum_time_error_less_than_100_nanosecond = 1
                estimated_maximum_time_error_less_than_1_microsecond = 2
                estimated_maximum_time_error_less_than_10_microsecond = 3
                estimated_maximum_time_error_less_than_100_microsecond = 4
                estimated_maximum_time_error_less_than_1_ms = 5
                estimated_maximum_time_error_less_than_10_ms = 6
                estimated_maximum_time_error_larger_than_10_ms_or_time_error_unknown = 7

            class TriggerReasonEnum(Enum):
                manual = 0
                magnitude_low = 1
                magnitude_high = 2
                phase_angle_diff = 3
                frequency_high_or_low = 4
                df_or_dt_high = 5
                reserved = 6
                digital = 7
                user_def_8 = 8
                user_def_9 = 9
                user_def_10 = 10
                user_def_11 = 11
                user_def_12 = 12
                user_def_13 = 13
                user_def_14 = 14
                user_def_15 = 15

            class PmuTriggerDetectedEnum(Enum):
                no_trigger = 0
                trigger_detected = 1

            class ConfigurationChangeEnum(Enum):
                change_effected = 0
                will_change_in_one_min = 1

            class DataModifiedEnum(Enum):
                not_modified = 0
                data_modified_by_post_processing = 1

            class PmuSyncEnum(Enum):
                in_sync_with_a_utc_traceable_time_source = 0
                not_in_sync_with_a_utc_traceable_time_source = 1

            class DataSortingEnum(Enum):
                by_time_stamp = 0
                by_arrival = 1

            class DataErrorEnum(Enum):
                good_measurement_data_no_errors = 0
                pmu_error_no_information_about_data_do_not_use = 1
                pmu_in_test_mode_or_absent_data_tags_have_been_insereted_do_not_use = 2
                pmu_error_do_not_use = 3

            class UnlockedTimeEnum(Enum):
                sync_locked_or_unlocked_less_than_10_s_best_quality = 0
                unlocked_time_less_than_100_s_larger_than_10_s = 1
                unlocked_time_less_than_1000_s_larger_than_100_s = 2
                unlocked_time_larger_than_1000_s = 3
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.data_error = self._root.PmuData.Stat.DataErrorEnum(self._io.read_bits_int(2))
                self.pmu_sync = self._root.PmuData.Stat.PmuSyncEnum(self._io.read_bits_int(1))
                self.data_sorting = self._root.PmuData.Stat.DataSortingEnum(self._io.read_bits_int(1))
                self.pmu_trigger_detected = self._root.PmuData.Stat.PmuTriggerDetectedEnum(self._io.read_bits_int(1))
                self.configuration_change = self._root.PmuData.Stat.ConfigurationChangeEnum(self._io.read_bits_int(1))
                self.data_modified = self._root.PmuData.Stat.DataModifiedEnum(self._io.read_bits_int(1))
                self.pmu_time_quality = self._root.PmuData.Stat.PmuTimeQualityEnum(self._io.read_bits_int(3))
                self.unlocked_time = self._root.PmuData.Stat.UnlockedTimeEnum(self._io.read_bits_int(2))
                self.trigger_reason = self._root.PmuData.Stat.TriggerReasonEnum(self._io.read_bits_int(4))


        class Dfreq(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                _on = self._parent._station.format.freq_data_type
                if _on == 'int':
                    self.dfreq = self._root.PmuData.Dfreq.Int(self._io, self, self._root)
                elif _on == 'float':
                    self.dfreq = self._root.PmuData.Dfreq.Float(self._io, self, self._root)

            class Int(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.raw_dfreq = self._io.read_s2be()

                @property
                def dfreq(self):
                    if hasattr(self, '_m_dfreq'):
                        return self._m_dfreq if hasattr(self, '_m_dfreq') else None

                    self._m_dfreq = (self.raw_dfreq / 100.0)
                    return self._m_dfreq if hasattr(self, '_m_dfreq') else None


            class Float(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.raw_dfreq = self._io.read_f4be()

                @property
                def dfreq(self):
                    if hasattr(self, '_m_dfreq'):
                        return self._m_dfreq if hasattr(self, '_m_dfreq') else None

                    self._m_dfreq = self.raw_dfreq
                    return self._m_dfreq if hasattr(self, '_m_dfreq') else None



        class Phasors(KaitaiStruct):
            @property
            def real(self):
                return self.phasors.phasors.real

            @property
            def imaginary(self):
                return self.phasors.phasors.imaginary

            @property
            def magnitude(self):
                return self.phasors.phasors.magnitude

            @property
            def angle(self):
                return self.phasors.phasors.angle


            def __init__(self, _io, _parent=None, _root=None, _phunit = None):
                self._phunit = _phunit
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                _on = self._parent._station.format.phasors_data_type
                if _on == 'int':
                    self.phasors = self._root.PmuData.Phasors.Int(self._io, self, self._root, self._phunit.conversion_factor)
                elif _on == 'float':
                    self.phasors = self._root.PmuData.Phasors.Float(self._io, self, self._root)

            class Int(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None, _conversion_factor = None):
                    self._conversion_factor = _conversion_factor
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    _on = self._parent._parent._station.format.rectangular_or_polar
                    if _on == 'rectangular':
                        self.phasors = self._root.PmuData.Phasors.Int.Rectangular(self._io, self, self._root, self._conversion_factor)
                    elif _on == 'polar':
                        self.phasors = self._root.PmuData.Phasors.Int.Polar(self._io, self, self._root, self._conversion_factor)

                class Rectangular(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None, _conversion_factor = None):
                        self._conversion_factor = _conversion_factor
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self.raw_real = self._io.read_s2be()
                        self.raw_imaginary = self._io.read_s2be()

                    @property
                    def real(self):
                        if hasattr(self, '_m_real'):
                            return self._m_real if hasattr(self, '_m_real') else None

                        self._m_real = self.raw_real * self._conversion_factor
                        return self._m_real if hasattr(self, '_m_real') else None

                    @property
                    def imaginary(self):
                        if hasattr(self, '_m_imaginary'):
                            return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                        self._m_imaginary = self.raw_imaginary * self._conversion_factor
                        return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                    @property
                    def magnitude(self):
                        if hasattr(self, '_m_magnitude'):
                            return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                        self._m_magnitude, self._m_angle = cmath.polar(complex(self.real,self.imaginary))
                        return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                    @property
                    def angle(self):
                        if hasattr(self, '_m_angle'):
                            return self._m_angle if hasattr(self, '_m_angle') else None

                        self._m_magnitude, self._m_angle = cmath.polar(complex(self.real, self.imaginary))
                        return self._m_angle if hasattr(self, '_m_angle') else None



                class Polar(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None,  _conversion_factor = None):
                        self._conversion_factor = _conversion_factor
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self.raw_magnitude = self._io.read_u2be()
                        self.angle = self._io.read_s2be()

                    @property
                    def real(self):
                        if hasattr(self, '_m_real'):
                            return self._m_real if hasattr(self, '_m_real') else None

                        z = cmath.rect(self.magnitude, self.angle)
                        self._m_real, self._m_imaginary = z.real, z.imag
                        return self._m_real if hasattr(self, '_m_real') else None

                    @property
                    def imaginary(self):
                        if hasattr(self, '_m_imaginary'):
                            return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                        z = cmath.rect(self.magnitude, self.angle)
                        self._m_real, self._m_imaginary = z.real, z.imag
                        return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                    @property
                    def magnitude(self):
                        if hasattr(self, '_m_magnitude'):
                            return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                        self._m_magnitude = self.raw_magnitude * self._conversion_factor
                        return self._m_magnitude if hasattr(self, '_m_magnitude') else None




            class Float(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    _on = self._parent._parent._station.format.rectangular_or_polar
                    if _on == 'rectangular':
                        self.phasors = self._root.PmuData.Phasors.Float.Rectangular(self._io, self, self._root)
                    elif _on == 'polar':
                        self.phasors = self._root.PmuData.Phasors.Float.Polar(self._io, self, self._root)

                class Rectangular(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self.real = self._io.read_f4be()
                        self.imaginary = self._io.read_f4be()

                    @property
                    def magnitude(self):
                        if hasattr(self, '_m_magnitude'):
                            return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                        self._m_magnitude, self._m_angle = cmath.polar(complex(self.real,self.imaginary))
                        return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                    @property
                    def angle(self):
                        if hasattr(self, '_m_angle'):
                            return self._m_angle if hasattr(self, '_m_angle') else None

                        self._m_magnitude, self._m_angle = cmath.polar(complex(self.real, self.imaginary))
                        return self._m_angle if hasattr(self, '_m_angle') else None


                class Polar(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self.magnitude = self._io.read_f4be()
                        self.angle = self._io.read_f4be()

                    @property
                    def real(self):
                        if hasattr(self, '_m_real'):
                            return self._m_real if hasattr(self, '_m_real') else None

                        z = cmath.rect(self.magnitude, self.angle)
                        self._m_real, self._m_imaginary = z.real, z.imag
                        return self._m_real if hasattr(self, '_m_real') else None

                    @property
                    def imaginary(self):
                        if hasattr(self, '_m_imaginary'):
                            return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                        z = cmath.rect(self.magnitude, self.angle)
                        self._m_real, self._m_imaginary = z.real, z.imag
                        return self._m_imaginary if hasattr(self, '_m_imaginary') else None





        class Analog(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None, _anunit = None):
                self._anunit = _anunit
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                _on = self._parent._station.format.analogs_data_type
                if _on == 'int':
                    self.analog = self._root.PmuData.Analog.Int(self._io, self, self._root, self._anunit.conversion_factor)
                elif _on == 'float':
                    self.analog = self._root.PmuData.Analog.Float(self._io, self, self._root)

            class Int(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None, _conversion_factor = None):
                    self._conversion_factor = _conversion_factor
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.raw_analog = self._io.read_bits_int(16)

                @property
                def analog(self):
                    if hasattr(self, '_m_analog'):
                        return self._m_analog if hasattr(self, '_m_analog') else None

                    self._m_analog = self.raw_analog * self._conversion_factor
                    return self._m_analog if hasattr(self, '_m_analog') else None




            class Float(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.analog = self._io.read_f4be()





